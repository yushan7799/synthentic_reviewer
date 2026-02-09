import React, { useState } from 'react';
import api from '../services/api';
import './PanelistCreator.css';

function PanelistCreator({ onPanelistCreated }) {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        profile_url: '',
        bio: '',
        expertise_areas: [],
        critical_score: 5,
        openness_score: 5,
        seriousness_score: 5,
    });
    const [expertiseInput, setExpertiseInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [extracting, setExtracting] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSliderChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: parseFloat(value) }));
    };

    const handleAddExpertise = () => {
        if (expertiseInput.trim()) {
            setFormData(prev => ({
                ...prev,
                expertise_areas: [...prev.expertise_areas, expertiseInput.trim()]
            }));
            setExpertiseInput('');
        }
    };

    const handleRemoveExpertise = (index) => {
        setFormData(prev => ({
            ...prev,
            expertise_areas: prev.expertise_areas.filter((_, i) => i !== index)
        }));
    };

    const handleExtractProfile = async () => {
        if (!formData.profile_url) {
            setError('Please enter a profile URL');
            return;
        }

        setExtracting(true);
        setError('');

        try {
            const response = await api.extractProfile(formData.profile_url);
            if (response.success) {
                const profile = response.profile;
                setFormData(prev => ({
                    ...prev,
                    name: profile.name || prev.name,
                    bio: profile.bio || prev.bio,
                    expertise_areas: [...new Set([...prev.expertise_areas, ...(profile.expertise_areas || [])])],
                }));
            }
        } catch (err) {
            setError('Failed to extract profile. Please enter details manually.');
        } finally {
            setExtracting(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await api.createPanelist(formData);
            if (response.success) {
                onPanelistCreated(response.panelist);
                // Reset form
                setFormData({
                    name: '',
                    email: '',
                    profile_url: '',
                    bio: '',
                    expertise_areas: [],
                    critical_score: 5,
                    openness_score: 5,
                    seriousness_score: 5,
                });
            }
        } catch (err) {
            setError(err.message || 'Failed to create panelist');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="panelist-creator glass-card">
            <h2>Create AI Panelist</h2>
            <p className="text-secondary mb-2">
                Add a new AI reviewer by providing their profile information and personality traits.
            </p>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                {/* Profile URL */}
                <div className="input-group">
                    <label className="input-label">Profile URL (LinkedIn, Google Scholar, etc.)</label>
                    <div className="url-input-group">
                        <input
                            type="url"
                            name="profile_url"
                            value={formData.profile_url}
                            onChange={handleInputChange}
                            className="input-field"
                            placeholder="https://scholar.google.com/..."
                        />
                        <button
                            type="button"
                            onClick={handleExtractProfile}
                            className="btn btn-secondary"
                            disabled={extracting || !formData.profile_url}
                        >
                            {extracting ? 'Extracting...' : 'Extract'}
                        </button>
                    </div>
                </div>

                {/* Name */}
                <div className="input-group">
                    <label className="input-label">Name *</label>
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        className="input-field"
                        placeholder="Dr. Jane Smith"
                        required
                    />
                </div>

                {/* Email */}
                <div className="input-group">
                    <label className="input-label">Email</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className="input-field"
                        placeholder="jane.smith@university.edu"
                    />
                </div>

                {/* Bio */}
                <div className="input-group">
                    <label className="input-label">Bio</label>
                    <textarea
                        name="bio"
                        value={formData.bio}
                        onChange={handleInputChange}
                        className="input-field"
                        placeholder="Professor of Computer Science at..."
                        rows="3"
                    />
                </div>

                {/* Expertise Areas */}
                <div className="input-group">
                    <label className="input-label">Expertise Areas</label>
                    <div className="expertise-input-group">
                        <input
                            type="text"
                            value={expertiseInput}
                            onChange={(e) => setExpertiseInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddExpertise())}
                            className="input-field"
                            placeholder="e.g., Machine Learning"
                        />
                        <button
                            type="button"
                            onClick={handleAddExpertise}
                            className="btn btn-secondary"
                        >
                            Add
                        </button>
                    </div>
                    <div className="expertise-tags">
                        {formData.expertise_areas.map((expertise, index) => (
                            <span key={index} className="expertise-tag">
                                {expertise}
                                <button
                                    type="button"
                                    onClick={() => handleRemoveExpertise(index)}
                                    className="remove-tag"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                </div>

                {/* Personality Traits */}
                <div className="personality-section">
                    <h3>Personality Traits</h3>
                    <p className="text-secondary">
                        Adjust these sliders to define the panelist's review style.
                    </p>

                    <div className="slider-group">
                        <label className="slider-label">
                            <span>Critical Score</span>
                            <span className="slider-value">{formData.critical_score}/10</span>
                        </label>
                        <input
                            type="range"
                            name="critical_score"
                            min="1"
                            max="10"
                            step="0.5"
                            value={formData.critical_score}
                            onChange={handleSliderChange}
                            className="range-slider"
                        />
                        <div className="slider-description">
                            <span>Supportive</span>
                            <span>Highly Critical</span>
                        </div>
                    </div>

                    <div className="slider-group">
                        <label className="slider-label">
                            <span>Openness Score</span>
                            <span className="slider-value">{formData.openness_score}/10</span>
                        </label>
                        <input
                            type="range"
                            name="openness_score"
                            min="1"
                            max="10"
                            step="0.5"
                            value={formData.openness_score}
                            onChange={handleSliderChange}
                            className="range-slider"
                        />
                        <div className="slider-description">
                            <span>Traditional</span>
                            <span>Very Open</span>
                        </div>
                    </div>

                    <div className="slider-group">
                        <label className="slider-label">
                            <span>Seriousness Score</span>
                            <span className="slider-value">{formData.seriousness_score}/10</span>
                        </label>
                        <input
                            type="range"
                            name="seriousness_score"
                            min="1"
                            max="10"
                            step="0.5"
                            value={formData.seriousness_score}
                            onChange={handleSliderChange}
                            className="range-slider"
                        />
                        <div className="slider-description">
                            <span>Casual</span>
                            <span>Very Thorough</span>
                        </div>
                    </div>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary btn-full"
                    disabled={loading || !formData.name}
                >
                    {loading ? 'Creating...' : 'Create Panelist'}
                </button>
            </form>
        </div>
    );
}

export default PanelistCreator;
