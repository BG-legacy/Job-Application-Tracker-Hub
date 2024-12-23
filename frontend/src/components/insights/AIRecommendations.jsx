import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import '../../styles/insights/AIRecommendations.css';

const AIRecommendations = () => {
    const [recommendations, setRecommendations] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchRecommendations();
    }, []);

    const fetchRecommendations = async () => {
        try {
            const response = await api.get('/ai-insights/recommendations/');
            setRecommendations(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching recommendations:', err);
            setError('Failed to fetch AI recommendations');
            setLoading(false);
        }
    };

    // Format percentage with 1 decimal place and handle edge cases
    const formatPercentage = (value) => {
        if (value === null || value === undefined || isNaN(value)) {
            return '0.0%';
        }
        return `${(value * 100).toFixed(1)}%`;
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!recommendations) return null;

    return (
        <div className="recommendations-container">
            <h2>Application Metrics</h2>
            <div className="metrics-grid">
                <div className="metric-card">
                    <h3>Response Rate</h3>
                    <div className="metric-value">
                        {formatPercentage(recommendations.metrics.response_rate)}
                    </div>
                </div>
                <div className="metric-card">
                    <h3>Interview Success</h3>
                    <div className="metric-value">
                        {formatPercentage(recommendations.metrics.interview_rate)}
                    </div>
                </div>
                <div className="metric-card">
                    <h3>Overall Success</h3>
                    <div className="metric-value">
                        {formatPercentage(recommendations.metrics.success_rate)}
                    </div>
                </div>
            </div>

            <div className="recommendations-section">
                <h2>AI Recommendations</h2>
                <div className="recommendations-list">
                    {recommendations.recommendations.split('\n\n').map((rec, index) => (
                        <div key={index} className="recommendation-card">
                            <div className="recommendation-type">
                                {rec.split(':')[0]}
                            </div>
                            <div className="recommendation-content">
                                {rec.split(':')[1]}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AIRecommendations; 