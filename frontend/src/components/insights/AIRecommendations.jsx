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
            const response = await api.get('/ai/recommendations/');
            setRecommendations(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching recommendations:', err);
            setError('Failed to fetch AI recommendations');
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading recommendations...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!recommendations) return null;

    return (
        <div className="ai-recommendations">
            <div className="metrics-section">
                <h2>Application Metrics</h2>
                <div className="metrics-grid">
                    <div className="metric-card">
                        <h3>Response Rate</h3>
                        <p>{(recommendations.metrics.response_rate * 100).toFixed(1)}%</p>
                    </div>
                    <div className="metric-card">
                        <h3>Interview Success</h3>
                        <p>{(recommendations.metrics.interview_conversion * 100).toFixed(1)}%</p>
                    </div>
                    <div className="metric-card">
                        <h3>Overall Success</h3>
                        <p>{(recommendations.metrics.success_rate * 100).toFixed(1)}%</p>
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