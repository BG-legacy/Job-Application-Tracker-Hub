import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './TeamsDashboard.css';

const TeamsDashboard = () => {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [newTeamData, setNewTeamData] = useState({ name: '', description: '' });
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchTeams();
    }, []);

    const fetchTeams = async () => {
        try {
            console.log('Fetching teams...');
            setLoading(true);
            const response = await api.get('/teams/');
            console.log('Teams response:', response.data);
            const teamsData = response.data.results || response.data || [];
            console.log('Processed teams data:', teamsData);
            setTeams(teamsData);
        } catch (err) {
            console.error('Error fetching teams:', err);
            console.error('Error details:', {
                message: err.message,
                response: err.response,
                status: err.response?.status
            });
            setError('Failed to fetch teams');
            setTeams([]);
        } finally {
            setLoading(false);
        }
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

    const handleManageMembers = async (teamId) => {
        try {
            console.log('Managing members for team:', teamId);
        } catch (err) {
            setError('Failed to manage team members');
            console.error('Error managing team members:', err);
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
                    Create Team
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}
            
            {loading ? (
                <div className="loading">Loading teams...</div>
            ) : (
                <div className="teams-grid">
                    {teams && teams.length > 0 ? (
                        teams.map(team => (
                            <div key={team.id} className="team-card">
                                <h3>{team.name}</h3>
                                <p>{team.description}</p>
                                <div className="team-stats">
                                    <span>{team.members?.length || 0} members</span>
                                </div>
                                <div className="team-actions">
                                    <button onClick={() => handleManageMembers(team.id)}>
                                        Manage Members
                                    </button>
                                </div>
                            </div>
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