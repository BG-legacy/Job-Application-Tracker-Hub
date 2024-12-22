import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import api from '../../services/api';
import '../../styles/teams/TeamDetails.css';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const TeamDetails = () => {
    const { teamId } = useParams();
    const [team, setTeam] = useState(null);
    const [tips, setTips] = useState([]);
    const [progress, setProgress] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [newTip, setNewTip] = useState('');

    const fetchTips = useCallback(async () => {
        try {
            const response = await api.get(`/teams/${teamId}/tips/`);
            const sortedTips = response.data.sort((a, b) => b.upvote_count - a.upvote_count);
            setTips(sortedTips);
        } catch (err) {
            console.error('Error fetching tips:', err);
        }
    }, [teamId]);

    const fetchTeamData = useCallback(async () => {
        try {
            const [teamResponse, progressResponse] = await Promise.all([
                api.get(`/teams/${teamId}/`),
                api.get(`/teams/${teamId}/progress/`)
            ]);
            
            setTeam(teamResponse.data);
            setProgress(progressResponse.data);
            await fetchTips();
        } catch (err) {
            setError('Failed to load team data');
        } finally {
            setLoading(false);
        }
    }, [teamId, fetchTips]);

    useEffect(() => {
        fetchTeamData();
    }, [fetchTeamData]);

    const handleUpvote = async (tipId) => {
        try {
            const response = await api.post(`/teams/${teamId}/tips/${tipId}/upvote/`);
            // Update the tips state with the updated tip data
            setTips(tips.map(tip => 
                tip.id === tipId ? response.data.tip : tip
            ));
        } catch (error) {
            console.error('Error upvoting tip:', error);
            // Add error handling as needed
        }
    };

    const handleAddTip = async (e) => {
        e.preventDefault();
        if (!newTip.trim()) return;

        try {
            const response = await api.post(`/teams/${teamId}/tips/`, {
                content: newTip
            });
            
            // Add the new tip to the list and sort by upvotes
            setTips(prevTips => [...prevTips, response.data]
                .sort((a, b) => b.upvote_count - a.upvote_count));
            setNewTip('');
        } catch (err) {
            console.error('Error adding tip:', err);
            setError('Failed to add tip');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!team) return <div>Team not found</div>;

    // Prepare data for the progress chart
    const chartData = {
        labels: progress?.status_breakdown.map(item => item.status) || [],
        datasets: [
            {
                label: 'Applications by Status',
                data: progress?.status_breakdown.map(item => item.count) || [],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }
        ]
    };

    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false
    };

    return (
        <div className="team-details">
            <header className="team-header">
                <h1>{team.name}</h1>
                <p>{team.description}</p>
            </header>

            <section className="team-progress">
                <h2>Team Progress</h2>
                <div className="progress-stats">
                    <div className="stat-card">
                        <h3>Total Applications</h3>
                        <p>{progress?.total_applications || 0}</p>
                    </div>
                    <div className="stat-card">
                        <h3>Interview Rate</h3>
                        <p>{progress?.interview_rate?.toFixed(1) || 0}%</p>
                    </div>
                    <div className="stat-card">
                        <h3>Offer Rate</h3>
                        <p>{progress?.offer_rate?.toFixed(1) || 0}%</p>
                    </div>
                </div>
                <div className="chart-container">
                    <Bar data={chartData} options={chartOptions} />
                </div>
            </section>

            <section className="tips-section">
                <h2>Team Tips</h2>
                <form onSubmit={handleAddTip} className="tip-form">
                    <div className="form-group">
                        <textarea
                            value={newTip}
                            onChange={(e) => setNewTip(e.target.value)}
                            placeholder="Share your tip with the team..."
                            className="tip-input"
                            rows="3"
                            required
                        />
                    </div>
                    <button type="submit" className="submit-tip-btn">
                        Share Tip
                    </button>
                </form>

                <div className="tips-list">
                    {tips.map(tip => (
                        <div key={tip.id} className="tip-card">
                            <div className="tip-content">
                                <p>{tip.content}</p>
                            </div>
                            <div className="tip-footer">
                                <div className="tip-meta">
                                    <span className="tip-author">By {tip.author_name}</span>
                                    <span className="tip-date">
                                        {new Date(tip.created_at).toLocaleDateString()}
                                    </span>
                                </div>
                                <button 
                                    onClick={() => handleUpvote(tip.id)}
                                    className={`upvote-btn ${tip.has_upvoted ? 'upvoted' : ''}`}
                                >
                                    <span className="upvote-icon">↑</span>
                                    <span className="upvote-count">{tip.upvote_count}</span>
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default TeamDetails; 