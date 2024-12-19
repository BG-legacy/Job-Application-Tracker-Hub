import api from './api';

export const teamService = {
    async getTeams() {
        const response = await fetch('/api/teams/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (!response.ok) throw new Error('Failed to fetch teams');
        return response.json();
    },

    async createTeam(formData) {
        console.log('FormData entries:');
        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        const response = await fetch('/api/teams/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });

        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);

        if (!response.ok) {
            const error = await response.json();
            console.error('Server error:', error);
            throw new Error(error.message || 'Failed to create team');
        }
        return response.json();
    },

    async addMember(teamId, email) {
        try {
            const response = await api.post(`/teams/${teamId}/add_member/`, { email });
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to add team member' };
        }
    }
}; 