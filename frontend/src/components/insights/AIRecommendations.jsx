import React, { useState, useEffect } from 'react';
import { aiInsightService } from '../../services/aiInsightService';
import '../../styles/insights/AIRecommendations.css';

const AIRecommendations = () => {
    const [insights, setInsights] = useState({
        recommendations: '',
        metrics: {
            response_rate: 0,
            interview_rate: 0,
            success_rate: 0,
            market_alignment: 0
        }
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchInsights();
    }, []);

    const fetchInsights = async () => {
        try {
            const response = await aiInsightService.getRecommendations();
            setInsights({
                recommendations: response.data.recommendations || '',
                metrics: {
                    response_rate: response.data.metrics?.response_rate || 0,
                    interview_rate: response.data.metrics?.interview_rate || 0,
                    success_rate: response.data.metrics?.success_rate || 0,
                    market_alignment: response.data.metrics?.market_alignment || 0
                }
            });
            setLoading(false);
        } catch (err) {
            setError('Failed to fetch AI recommendations');
            setLoading(false);
        }
    };

    const formatMetric = (value) => {
        return typeof value === 'number' ? value.toFixed(1) : '0.0';
    };

    if (loading) return <div className="loading">Loading insights...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="ai-recommendations">
            <h2>AI-Powered Insights</h2>
            
            <div className="metrics-section">
                <h3>Application Metrics</h3>
                <div className="metrics-grid">
                    <div className="metric-card">
                        <h4>Response Rate</h4>
                        <p>{formatMetric(insights.metrics.response_rate)}%</p>
                    </div>
                    <div className="metric-card">
                        <h4>Interview Rate</h4>
                        <p>{formatMetric(insights.metrics.interview_rate)}%</p>
                    </div>
                    <div className="metric-card">
                        <h4>Success Rate</h4>
                        <p>{formatMetric(insights.metrics.success_rate)}%</p>
                    </div>
                    <div className="metric-card">
                        <h4>Market Alignment</h4>
                        <p>{formatMetric(insights.metrics.market_alignment)}%</p>
                    </div>
                </div>
            </div>

            <div className="recommendations-section">
                <h3>AI Recommendation</h3>
                <div className="recommendation-card">
                    <p>{insights.recommendations}</p>
                </div>
            </div>
        </div>
    );
};

export default AIRecommendations; 