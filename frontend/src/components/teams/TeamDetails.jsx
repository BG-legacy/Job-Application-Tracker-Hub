import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import api from '../../services/api';
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
            setTips(response.data);
        } catch (err) {
            console.error('Failed to fetch tips:', err);
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
            const response = await api.patch(`/teams/${teamId}/tips/${tipId}/rate/`);
            setTips(prevTips => 
                prevTips.map(tip => 
                    tip.id === tipId ? response.data.tip : tip
                )
            );
        } catch (err) {
            console.error('Failed to upvote tip:', err);
        }
    };

    const handleAddTip = async (e) => {
        e.preventDefault();
        try {
            await api.post(`/teams/${teamId}/tips/`, { content: newTip });
            setNewTip('');
            await fetchTips();
        } catch (err) {
            console.error('Failed to add tip:', err);
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
                label: 'Team Applications',
                data: progress?.status_breakdown.map(item => item.count) || [],
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Team Application Status Distribution'
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    };

    return (
        <div className="team-details">
            <header className="team-header">
                <h1>{team.name}</h1>
                <p>{team.description}</p>
            </header>

            <section className="team-stats">
                <div className="stats-grid">
                    <div className="stat-card">
                        <h3>Total Applications</h3>
                        <p>{progress?.total_applications || 0}</p>
                    </div>
                    <div className="stat-card">
                        <h3>Active Members</h3>
                        <p>{progress?.active_members || 0}</p>
                    </div>
                    <div className="stat-card">
                        <h3>Interview Rate</h3>
                        <p>{(progress?.interview_rate || 0).toFixed(1)}%</p>
                    </div>
                    <div className="stat-card">
                        <h3>Offer Rate</h3>
                        <p>{(progress?.offer_rate || 0).toFixed(1)}%</p>
                    </div>
                </div>

                <div className="chart-container">
                    <Bar data={chartData} options={chartOptions} />
                </div>
            </section>

            <section className="team-tips">
                <h2>Team Tips</h2>
                <form onSubmit={handleAddTip} className="add-tip-form">
                    <input
                        type="text"
                        value={newTip}
                        onChange={(e) => setNewTip(e.target.value)}
                        placeholder="Share a tip with your team..."
                        required
                    />
                    <button type="submit">Share Tip</button>
                </form>

                <div className="tips-list">
                    {tips
                        .sort((a, b) => b.upvote_count - a.upvote_count)
                        .map(tip => (
                            <div key={tip.id} className="tip-card">
                                <p>{tip.content}</p>
                                <div className="tip-meta">
                                    <span>By {tip.author_name}</span>
                                    <button 
                                        onClick={() => handleUpvote(tip.id)}
                                        className={`upvote-btn ${tip.has_upvoted ? 'upvoted' : ''}`}
                                    >
                                        ↑ {tip.upvote_count}
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