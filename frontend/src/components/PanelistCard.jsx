import React from 'react';
import './PanelistCard.css';

function PanelistCard({ panelist, onDelete, onSelect }) {
    const { personality } = panelist;

    const getPersonalityColor = (score) => {
        if (score >= 7) return 'var(--accent)';
        if (score <= 3) return 'var(--secondary)';
        return 'var(--primary)';
    };

    return (
        <div className="panelist-card glass-card" onClick={() => onSelect && onSelect(panelist)}>
            <div className="panelist-header">
                <div className="panelist-avatar">
                    {panelist.name.charAt(0).toUpperCase()}
                </div>
                <div className="panelist-info">
                    <h3>{panelist.name}</h3>
                    {panelist.email && <p className="text-secondary">{panelist.email}</p>}
                </div>
            </div>

            {panelist.bio && (
                <p className="panelist-bio text-secondary">
                    {panelist.bio.length > 150 ? panelist.bio.substring(0, 150) + '...' : panelist.bio}
                </p>
            )}

            {panelist.expertise_areas && panelist.expertise_areas.length > 0 && (
                <div className="expertise-list">
                    {panelist.expertise_areas.slice(0, 3).map((expertise, index) => (
                        <span key={index} className="expertise-badge">
                            {expertise}
                        </span>
                    ))}
                    {panelist.expertise_areas.length > 3 && (
                        <span className="expertise-badge">+{panelist.expertise_areas.length - 3}</span>
                    )}
                </div>
            )}

            <div className="personality-bars">
                <div className="personality-bar">
                    <div className="bar-label">
                        <span>Critical</span>
                        <span>{personality.critical_score}/10</span>
                    </div>
                    <div className="bar-track">
                        <div
                            className="bar-fill"
                            style={{
                                width: `${personality.critical_score * 10}%`,
                                background: getPersonalityColor(personality.critical_score)
                            }}
                        />
                    </div>
                </div>

                <div className="personality-bar">
                    <div className="bar-label">
                        <span>Openness</span>
                        <span>{personality.openness_score}/10</span>
                    </div>
                    <div className="bar-track">
                        <div
                            className="bar-fill"
                            style={{
                                width: `${personality.openness_score * 10}%`,
                                background: getPersonalityColor(personality.openness_score)
                            }}
                        />
                    </div>
                </div>

                <div className="personality-bar">
                    <div className="bar-label">
                        <span>Seriousness</span>
                        <span>{personality.seriousness_score}/10</span>
                    </div>
                    <div className="bar-track">
                        <div
                            className="bar-fill"
                            style={{
                                width: `${personality.seriousness_score * 10}%`,
                                background: getPersonalityColor(personality.seriousness_score)
                            }}
                        />
                    </div>
                </div>
            </div>

            {onDelete && (
                <button
                    className="delete-btn"
                    onClick={(e) => {
                        e.stopPropagation();
                        onDelete(panelist.id);
                    }}
                >
                    Delete
                </button>
            )}
        </div>
    );
}

export default PanelistCard;
