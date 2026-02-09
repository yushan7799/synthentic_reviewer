import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './ReviewDisplay.css';

function ReviewDisplay({ proposalId }) {
    const [reviews, setReviews] = useState([]);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [generating, setGenerating] = useState(false);
    const [panelists, setPanelists] = useState([]);
    const [selectedPanelists, setSelectedPanelists] = useState([]);

    useEffect(() => {
        loadReviews();
        loadPanelists();
    }, [proposalId]);

    const loadReviews = async () => {
        try {
            const response = await api.getProposalReviews(proposalId);
            if (response.success) {
                setSummary(response.summary);
                setReviews(response.summary.reviews || []);
            }
        } catch (err) {
            console.error('Failed to load reviews:', err);
        } finally {
            setLoading(false);
        }
    };

    const loadPanelists = async () => {
        try {
            const response = await api.getPanelists();
            if (response.success) {
                setPanelists(response.panelists);
            }
        } catch (err) {
            console.error('Failed to load panelists:', err);
        }
    };

    const handleGenerateReviews = async () => {
        setGenerating(true);
        try {
            const response = await api.generatePanelReview(
                proposalId,
                selectedPanelists.length > 0 ? selectedPanelists : null
            );
            if (response.success) {
                await loadReviews();
            }
        } catch (err) {
            console.error('Failed to generate reviews:', err);
        } finally {
            setGenerating(false);
        }
    };

    const getRecommendationColor = (recommendation) => {
        switch (recommendation) {
            case 'accept': return 'var(--success)';
            case 'reject': return 'var(--error)';
            default: return 'var(--warning)';
        }
    };

    const getScoreColor = (score) => {
        if (score >= 8) return 'var(--success)';
        if (score >= 6) return 'var(--primary)';
        if (score >= 4) return 'var(--warning)';
        return 'var(--error)';
    };

    if (loading) {
        return (
            <div className="review-display glass-card">
                <div className="loading-container">
                    <div className="spinner"></div>
                    <p>Loading reviews...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="review-display">
            {reviews.length === 0 ? (
                <div className="glass-card">
                    <h2>Generate Reviews</h2>
                    <p className="text-secondary mb-2">
                        Select panelists to review this proposal, or generate reviews from all panelists.
                    </p>

                    <div className="panelist-selector">
                        {panelists.map(panelist => (
                            <label key={panelist.id} className="panelist-checkbox">
                                <input
                                    type="checkbox"
                                    checked={selectedPanelists.includes(panelist.id)}
                                    onChange={(e) => {
                                        if (e.target.checked) {
                                            setSelectedPanelists([...selectedPanelists, panelist.id]);
                                        } else {
                                            setSelectedPanelists(selectedPanelists.filter(id => id !== panelist.id));
                                        }
                                    }}
                                />
                                <span>{panelist.name}</span>
                            </label>
                        ))}
                    </div>

                    <button
                        className="btn btn-primary btn-full"
                        onClick={handleGenerateReviews}
                        disabled={generating || panelists.length === 0}
                    >
                        {generating ? (
                            <>
                                <span className="spinner-small"></span>
                                Generating Reviews...
                            </>
                        ) : (
                            `Generate Reviews ${selectedPanelists.length > 0 ? `(${selectedPanelists.length} panelists)` : '(All panelists)'}`
                        )}
                    </button>
                </div>
            ) : (
                <>
                    {/* Summary Card */}
                    <div className="glass-card summary-card">
                        <h2>Review Summary</h2>
                        <div className="summary-stats">
                            <div className="stat-item">
                                <div className="score-circle" style={{ background: `linear-gradient(135deg, ${getScoreColor(summary.average_score)}, var(--primary-dark))` }}>
                                    {summary.average_score.toFixed(1)}
                                </div>
                                <p className="stat-label">Average Score</p>
                            </div>

                            <div className="stat-item">
                                <div className="stat-value">{summary.review_count}</div>
                                <p className="stat-label">Reviews</p>
                            </div>

                            <div className="stat-item">
                                <div className="recommendation-breakdown">
                                    {Object.entries(summary.recommendation_breakdown).map(([rec, count]) => (
                                        <div key={rec} className="rec-item">
                                            <span className="badge" style={{ background: getRecommendationColor(rec) }}>
                                                {rec}
                                            </span>
                                            <span>{count}</span>
                                        </div>
                                    ))}
                                </div>
                                <p className="stat-label">Recommendations</p>
                            </div>
                        </div>

                        {summary.category_averages && (
                            <div className="category-scores">
                                <h3>Category Averages</h3>
                                <div className="category-grid">
                                    {Object.entries(summary.category_averages).map(([category, score]) => (
                                        <div key={category} className="category-item">
                                            <div className="category-label">{category}</div>
                                            <div className="category-bar">
                                                <div
                                                    className="category-fill"
                                                    style={{
                                                        width: `${score * 10}%`,
                                                        background: getScoreColor(score)
                                                    }}
                                                />
                                            </div>
                                            <div className="category-score">{score.toFixed(1)}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Individual Reviews */}
                    <div className="reviews-list">
                        <h2>Individual Reviews</h2>
                        {reviews.map((review, index) => {
                            const panelist = panelists.find(p => p.id === review.panelist_id);
                            return (
                                <div key={review.id} className="review-card glass-card fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                                    <div className="review-header">
                                        <div className="reviewer-info">
                                            <div className="reviewer-avatar">
                                                {panelist?.name.charAt(0).toUpperCase() || 'R'}
                                            </div>
                                            <div>
                                                <h3>{panelist?.name || 'Reviewer'}</h3>
                                                <p className="text-secondary">
                                                    {panelist?.expertise_areas?.slice(0, 2).join(', ')}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="review-score">
                                            <div className="score-circle" style={{ background: `linear-gradient(135deg, ${getScoreColor(review.overall_score)}, var(--primary-dark))` }}>
                                                {review.overall_score.toFixed(1)}
                                            </div>
                                            <span
                                                className="badge"
                                                style={{ background: getRecommendationColor(review.recommendation) }}
                                            >
                                                {review.recommendation}
                                            </span>
                                        </div>
                                    </div>

                                    {review.feedback.summary && (
                                        <div className="review-section">
                                            <h4>Summary</h4>
                                            <p>{review.feedback.summary}</p>
                                        </div>
                                    )}

                                    <div className="review-scores-grid">
                                        {Object.entries(review.scores).map(([category, score]) => (
                                            score && (
                                                <div key={category} className="score-item">
                                                    <span className="score-label">{category}</span>
                                                    <span className="score-value" style={{ color: getScoreColor(score) }}>
                                                        {score.toFixed(1)}
                                                    </span>
                                                </div>
                                            )
                                        ))}
                                    </div>

                                    {review.feedback.strengths && review.feedback.strengths.length > 0 && (
                                        <div className="review-section">
                                            <h4>✅ Strengths</h4>
                                            <ul>
                                                {review.feedback.strengths.map((strength, i) => (
                                                    <li key={i}>{strength}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {review.feedback.weaknesses && review.feedback.weaknesses.length > 0 && (
                                        <div className="review-section">
                                            <h4>⚠️ Weaknesses</h4>
                                            <ul>
                                                {review.feedback.weaknesses.map((weakness, i) => (
                                                    <li key={i}>{weakness}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}

                                    {review.feedback.detailed_comments && (
                                        <div className="review-section">
                                            <h4>Detailed Comments</h4>
                                            <p>{review.feedback.detailed_comments}</p>
                                        </div>
                                    )}

                                    {review.feedback.suggestions && (
                                        <div className="review-section">
                                            <h4>💡 Suggestions</h4>
                                            <p>{review.feedback.suggestions}</p>
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </>
            )}
        </div>
    );
}

export default ReviewDisplay;
