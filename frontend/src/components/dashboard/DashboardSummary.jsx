import React, { useState, useEffect } from 'react';
import { Chart as ChartJS } from 'chart.js/auto';
import { Pie, Line } from 'react-chartjs-2';
import api from '../../services/api';
import '../../styles/dashboard/DashboardSummary.css';

ChartJS.register();

const DashboardSummary = () => {
    const [summaryData, setSummaryData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchSummaryData();
    }, []);

    const fetchSummaryData = async () => {
        try {
            const response = await api.get('/ai-insights/dashboard/summary/');
            setSummaryData(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Dashboard fetch error:', err);
            setError('Failed to load dashboard data');
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!summaryData) return null;

    const statusChartData = {
        labels: Object.keys(summaryData.status_breakdown),
        datasets: [{
            data: Object.values(summaryData.status_breakdown),
            backgroundColor: [
                '#4CAF50', // Accepted
                '#2196F3', // Interview
                '#FFC107', // Pending
                '#F44336', // Rejected
                '#9C27B0', // Offer
                '#607D8B'  // Withdrawn
            ]
        }]
    };

    const monthlyTrendData = {
        labels: Object.keys(summaryData.monthly_applications),
        datasets: [{
            label: 'Applications per Month',
            data: Object.values(summaryData.monthly_applications),
            borderColor: '#2196F3',
            tension: 0.1
        }]
    };

    return (
        <div className="dashboard-summary">
            <div className="summary-header">
                <h2>Application Summary</h2>
                <div className="key-metrics">
                    <div className="metric-card">
                        <h3>Total Applications</h3>
                        <p>{summaryData.total_applications}</p>
                    </div>
                    <div className="metric-card">
                        <h3>Response Rate</h3>
                        <p>{summaryData.response_rate}%</p>
                    </div>
                    <div className="metric-card">
                        <h3>Recent Applications</h3>
                        <p>{summaryData.recent_applications}</p>
                    </div>
                </div>
            </div>

            <div className="charts-container">
                <div className="chart-card">
                    <h3>Application Status Distribution</h3>
                    <Pie 
                        data={statusChartData}
                        options={{
                            plugins: {
                                legend: {
                                    position: 'right'
                                }
                            }
                        }}
                    />
                </div>

                <div className="chart-card">
                    <h3>Monthly Application Trend</h3>
                    <Line 
                        data={monthlyTrendData}
                        options={{
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: {
                                        stepSize: 1
                                    }
                                }
                            }
                        }}
                    />
                </div>
            </div>

            <div className="top-positions">
                <h3>Top Applied Positions</h3>
                <div className="positions-list">
                    {Object.entries(summaryData.top_positions).map(([position, count]) => (
                        <div key={position} className="position-item">
                            <span>{position}</span>
                            <span>{count} applications</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default DashboardSummary; 