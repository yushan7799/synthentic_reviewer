import React, { useState, useEffect } from 'react';
import api from './services/api';
import PanelistCreator from './components/PanelistCreator';
import PanelistCard from './components/PanelistCard';
import ProposalUploader from './components/ProposalUploader';
import ReviewDisplay from './components/ReviewDisplay';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [panelists, setPanelists] = useState([]);
    const [proposals, setProposals] = useState([]);
    const [selectedProposal, setSelectedProposal] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [panelistsRes, proposalsRes] = await Promise.all([
                api.getPanelists(),
                api.getProposals()
            ]);

            if (panelistsRes.success) {
                setPanelists(panelistsRes.panelists);
            }

            if (proposalsRes.success) {
                setProposals(proposalsRes.proposals);
            }
        } catch (err) {
            console.error('Failed to load data:', err);
        } finally {
            setLoading(false);
        }
    };

    const handlePanelistCreated = (panelist) => {
        setPanelists([...panelists, panelist]);
        setActiveTab('panelists');
    };

    const handlePanelistDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this panelist?')) {
            try {
                await api.deletePanelist(id);
                setPanelists(panelists.filter(p => p.id !== id));
            } catch (err) {
                console.error('Failed to delete panelist:', err);
            }
        }
    };

    const handleProposalUploaded = (proposal) => {
        setProposals([...proposals, proposal]);
        setSelectedProposal(proposal);
        setActiveTab('reviews');
    };

    const handleProposalDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this proposal?')) {
            try {
                await api.deleteProposal(id);
                setProposals(proposals.filter(p => p.id !== id));
                if (selectedProposal?.id === id) {
                    setSelectedProposal(null);
                }
            } catch (err) {
                console.error('Failed to delete proposal:', err);
            }
        }
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="container">
                    <div className="header-content">
                        <div className="logo">
                            <h1>🔬 Synthetic Reviewer</h1>
                            <p className="tagline">AI-Powered Proposal Review System</p>
                        </div>
                        <div className="header-stats">
                            <div className="stat">
                                <span className="stat-number">{panelists.length}</span>
                                <span className="stat-label">Panelists</span>
                            </div>
                            <div className="stat">
                                <span className="stat-number">{proposals.length}</span>
                                <span className="stat-label">Proposals</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Navigation */}
            <nav className="app-nav">
                <div className="container">
                    <div className="nav-tabs">
                        <button
                            className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
                            onClick={() => setActiveTab('dashboard')}
                        >
                            📊 Dashboard
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'panelists' ? 'active' : ''}`}
                            onClick={() => setActiveTab('panelists')}
                        >
                            👥 Panelists
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'create-panelist' ? 'active' : ''}`}
                            onClick={() => setActiveTab('create-panelist')}
                        >
                            ➕ Create Panelist
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'upload' ? 'active' : ''}`}
                            onClick={() => setActiveTab('upload')}
                        >
                            📤 Upload Proposal
                        </button>
                        <button
                            className={`nav-tab ${activeTab === 'reviews' ? 'active' : ''}`}
                            onClick={() => setActiveTab('reviews')}
                            disabled={!selectedProposal}
                        >
                            📝 Reviews
                        </button>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="app-main">
                <div className="container">
                    {loading ? (
                        <div className="loading-screen">
                            <div className="spinner"></div>
                            <p>Loading...</p>
                        </div>
                    ) : (
                        <>
                            {activeTab === 'dashboard' && (
                                <div className="dashboard fade-in">
                                    <div className="welcome-card glass-card">
                                        <h2>Welcome to Synthetic Reviewer</h2>
                                        <p className="text-secondary">
                                            An AI-powered system that simulates scientific proposal review processes
                                            using AI panelists with distinct personalities and expertise profiles.
                                        </p>
                                        <div className="quick-actions">
                                            <button
                                                className="btn btn-primary"
                                                onClick={() => setActiveTab('create-panelist')}
                                            >
                                                Create Your First Panelist
                                            </button>
                                            <button
                                                className="btn btn-secondary"
                                                onClick={() => setActiveTab('upload')}
                                                disabled={panelists.length === 0}
                                            >
                                                Upload a Proposal
                                            </button>
                                        </div>
                                    </div>

                                    {panelists.length > 0 && (
                                        <div className="section">
                                            <h2>Your Panelists</h2>
                                            <div className="grid grid-3">
                                                {panelists.slice(0, 6).map(panelist => (
                                                    <PanelistCard
                                                        key={panelist.id}
                                                        panelist={panelist}
                                                        onDelete={handlePanelistDelete}
                                                    />
                                                ))}
                                            </div>
                                            {panelists.length > 6 && (
                                                <button
                                                    className="btn btn-secondary mt-2"
                                                    onClick={() => setActiveTab('panelists')}
                                                >
                                                    View All Panelists
                                                </button>
                                            )}
                                        </div>
                                    )}

                                    {proposals.length > 0 && (
                                        <div className="section">
                                            <h2>Recent Proposals</h2>
                                            <div className="proposals-list">
                                                {proposals.slice(0, 5).map(proposal => (
                                                    <div key={proposal.id} className="proposal-item glass-card">
                                                        <div className="proposal-header">
                                                            <h3>{proposal.title}</h3>
                                                            <span className={`badge badge-${proposal.status === 'completed' ? 'success' : 'warning'}`}>
                                                                {proposal.status}
                                                            </span>
                                                        </div>
                                                        {proposal.abstract && (
                                                            <p className="text-secondary">
                                                                {proposal.abstract.substring(0, 150)}...
                                                            </p>
                                                        )}
                                                        <div className="proposal-actions">
                                                            <button
                                                                className="btn btn-primary"
                                                                onClick={() => {
                                                                    setSelectedProposal(proposal);
                                                                    setActiveTab('reviews');
                                                                }}
                                                            >
                                                                View Reviews
                                                            </button>
                                                            <button
                                                                className="btn btn-secondary"
                                                                onClick={() => handleProposalDelete(proposal.id)}
                                                            >
                                                                Delete
                                                            </button>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}

                            {activeTab === 'panelists' && (
                                <div className="panelists-view fade-in">
                                    <div className="section-header">
                                        <h2>All Panelists</h2>
                                        <button
                                            className="btn btn-primary"
                                            onClick={() => setActiveTab('create-panelist')}
                                        >
                                            ➕ Create New Panelist
                                        </button>
                                    </div>
                                    {panelists.length === 0 ? (
                                        <div className="empty-state glass-card">
                                            <p>No panelists yet. Create your first panelist to get started!</p>
                                        </div>
                                    ) : (
                                        <div className="grid grid-3">
                                            {panelists.map(panelist => (
                                                <PanelistCard
                                                    key={panelist.id}
                                                    panelist={panelist}
                                                    onDelete={handlePanelistDelete}
                                                />
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            {activeTab === 'create-panelist' && (
                                <div className="fade-in">
                                    <PanelistCreator onPanelistCreated={handlePanelistCreated} />
                                </div>
                            )}

                            {activeTab === 'upload' && (
                                <div className="fade-in">
                                    <ProposalUploader onProposalUploaded={handleProposalUploaded} />
                                </div>
                            )}

                            {activeTab === 'reviews' && selectedProposal && (
                                <div className="fade-in">
                                    <div className="proposal-header-card glass-card mb-2">
                                        <h2>{selectedProposal.title}</h2>
                                        {selectedProposal.abstract && (
                                            <p className="text-secondary">{selectedProposal.abstract}</p>
                                        )}
                                    </div>
                                    <ReviewDisplay proposalId={selectedProposal.id} />
                                </div>
                            )}
                        </>
                    )}
                </div>
            </main>

            {/* Footer */}
            <footer className="app-footer">
                <div className="container">
                    <p className="text-secondary text-center">
                        Synthetic Reviewer - AI-Powered Proposal Review System
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
