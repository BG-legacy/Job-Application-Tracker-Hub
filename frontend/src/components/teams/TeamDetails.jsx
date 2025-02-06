import React, { useState, useEffect, useCallback, useMemo } from 'react';
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
import { useAuth } from '../../contexts/AuthContext';

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
    const [showInviteModal, setShowInviteModal] = useState(false);
    const { user } = useAuth();

    // Check if current user is admin
    const isAdmin = useMemo(() => {
        if (!team || !user) return false;
        const currentMember = team.members.find(member => member.user_details.id === user.id);
        return currentMember?.role === 'Admin';
    }, [team, user]);

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
            await api.post(`/teams/${teamId}/tips/${tipId}/upvote/`);
            // Refresh tips after upvoting
            await fetchTips();
        } catch (error) {
            console.error('Error upvoting tip:', error);
        }
    };

    const handleAddTip = async (e) => {
        e.preventDefault();
        if (!newTip.trim()) return;

        try {
            await api.post(`/teams/${teamId}/tips/`, {
                content: newTip
            });
            
            setNewTip('');
            // Refresh tips after adding new one
            await fetchTips();
        } catch (error) {
            console.error('Error adding tip:', error);
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
                    stepSize: 1,
                    font: {
                        size: 12
                    }
                },
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 12
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Application Status Distribution',
                font: {
                    size: 16,
                    weight: 'normal'
                },
                padding: {
                    bottom: 20
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        barThickness: 40,
        backgroundColor: [
            'rgba(99, 102, 241, 0.5)',  // Indigo
            'rgba(234, 179, 8, 0.5)',   // Yellow
            'rgba(34, 197, 94, 0.5)',   // Green
            'rgba(239, 68, 68, 0.5)'    // Red
        ],
        borderColor: [
            'rgba(99, 102, 241, 1)',
            'rgba(234, 179, 8, 1)',
            'rgba(34, 197, 94, 1)',
            'rgba(239, 68, 68, 1)'
        ],
        borderWidth: 1,
        hoverBackgroundColor: [
            'rgba(99, 102, 241, 0.7)',
            'rgba(234, 179, 8, 0.7)',
            'rgba(34, 197, 94, 0.7)',
            'rgba(239, 68, 68, 0.7)'
        ]
    };

    return (
        <div className="team-details">
            <header className="team-header">
                <h1>{team?.name}</h1>
                <p>{team?.description}</p>
            </header>

            <div className="team-grid">
                <section className="team-members-section">
                    <div className="section-header">
                        <h2>Team Members</h2>
                        {isAdmin && (
                            <button 
                                className="create-team-btn"
                                onClick={() => setShowInviteModal(true)}
                            >
                                Add Member
                            </button>
                        )}
                    </div>
                    <div className="member-list">
                        {team?.members.map(member => (
                            <div key={member.id} className="member-card">
                                <div className="member-avatar">
                                    {member.user_details.username.charAt(0).toUpperCase()}
                                </div>
                                <div className="member-info">
                                    <div className="member-name">{member.user_details.username}</div>
                                    <div className="member-role">{member.role}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                <section className="applications-section">
                    <div className="section-header">
                        <h2>Recent Applications</h2>
                    </div>
                    <div className="application-list">
                        {progress?.status_breakdown.map((item, index) => (
                            <div key={index} className="application-card">
                                <div className="application-info">
                                    <div className="company-name">
                                        {item.status}
                                    </div>
                                    <div className="position-title">
                                        {item.count} applications
                                    </div>
                                </div>
                                <div className={`application-status status-${item.status.toLowerCase()}`}>
                                    {item.count}
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </div>

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
                    <textarea
                        value={newTip}
                        onChange={(e) => setNewTip(e.target.value)}
                        placeholder="Share your insights and tips with the team..."
                        className="tip-input"
                        rows="4"
                        required
                    />
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
                                        {new Date(tip.created_at).toLocaleDateString(undefined, {
                                            year: 'numeric',
                                            month: 'short',
                                            day: 'numeric'
                                        })}
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