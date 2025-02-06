import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import './TeamsDashboard.css';

const TeamCard = ({ team, onManage }) => (
    <div className="team-card">
        <h3>{team.name}</h3>
        <p>{team.description}</p>
        <div className="team-stats">
            <div className="stat-item">
                <div className="stat-label">Members</div>
                <div className="stat-value">{team.member_count || 0}</div>
            </div>
            <div className="stat-item">
                <div className="stat-label">Applications</div>
                <div className="stat-value">{team.application_count || 0}</div>
            </div>
            <div className="stat-item">
                <div className="stat-label">Success Rate</div>
                <div className="stat-value">{team.success_rate || 0}%</div>
            </div>
        </div>
        <div className="team-card-actions">
            <button 
                className="manage-team-btn"
                onClick={() => onManage(team.id)}
            >
                Manage Team
            </button>
        </div>
    </div>
);

const TeamsDashboard = () => {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [newTeamData, setNewTeamData] = useState({ name: '', description: '' });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchTeams();
    }, []);

    const fetchTeams = async () => {
        try {
            setLoading(true);
            const response = await api.get('/teams/');
            setTeams(response.data.results || response.data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching teams:', err);
            setError('Failed to fetch teams');
            setTeams([]);
            setLoading(false);
        }
    };

    const handleManageTeam = (teamId) => {
        navigate(`/teams/${teamId}`);
    };

    const handleCreateTeam = async (e) => {
        e.preventDefault();
        try {
            console.log('Creating team with data:', newTeamData);
            const response = await api.post('/teams/', newTeamData);
            console.log('Create team response:', response.data);
            setShowCreateModal(false);
            setNewTeamData({ name: '', description: '' });
            setTeams(prevTeams => [...prevTeams, response.data]);
        } catch (err) {
            console.error('Error creating team:', err);
            console.error('Error details:', {
                message: err.message,
                response: err.response?.data,
                status: err.response?.status,
                headers: err.response?.headers
            });
            setError(err.response?.data?.error || 'Failed to create team');
        }
    };

    return (
        <div className="teams-dashboard">
            <div className="teams-header">
                <h1>My Teams</h1>
                <button 
                    className="create-team-btn"
                    onClick={() => setShowCreateModal(true)}
                >
                    Create New Team
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}
            
            {loading ? (
                <div className="loading">Loading teams...</div>
            ) : (
                <div className="teams-grid">
                    {teams && teams.length > 0 ? (
                        teams.map(team => (
                            <TeamCard key={team.id} team={team} onManage={handleManageTeam} />
                        ))
                    ) : (
                        <div className="no-teams-message">
                            No teams found. Create a team to get started!
                        </div>
                    )}
                </div>
            )}

            {showCreateModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>Create New Team</h2>
                        <form onSubmit={handleCreateTeam}>
                            <input
                                type="text"
                                placeholder="Team Name"
                                value={newTeamData.name}
                                onChange={(e) => setNewTeamData({
                                    ...newTeamData,
                                    name: e.target.value
                                })}
                                required
                            />
                            <textarea
                                placeholder="Team Description"
                                value={newTeamData.description}
                                onChange={(e) => setNewTeamData({
                                    ...newTeamData,
                                    description: e.target.value
                                })}
                            />
                            <div className="modal-actions">
                                <button type="submit">Create</button>
                                <button 
                                    type="button"
                                    onClick={() => setShowCreateModal(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TeamsDashboard; 