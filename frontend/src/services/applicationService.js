import api from './api';

export const applicationService = {
    async getApplications() {
        try {
            const response = await api.get('/applications/');
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to fetch applications' };
        }
    },

    async createApplication(applicationData) {
        try {
            const response = await api.post('/applications/', applicationData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to create application' };
        }
    },

    async updateApplication(id, applicationData) {
        try {
            const response = await api.put(`/applications/${id}/`, applicationData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to update application' };
        }
    },

    async deleteApplication(id) {
        try {
            await api.delete(`/applications/${id}/`);
        } catch (error) {
            throw error.response?.data || { message: 'Failed to delete application' };
        }
    }
}; 