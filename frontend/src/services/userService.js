import api from './api';

export const userService = {
    async getProfile() {
        try {
            const response = await api.get('/users/profile/');
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to fetch profile' };
        }
    },

    async updateProfile(profileData) {
        try {
            const response = await api.put('/users/profile/', profileData);
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to update profile' };
        }
    },

    async updateAvatar(formData) {
        try {
            const response = await api.put('/users/profile/avatar/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: 'Failed to update avatar' };
        }
    }
}; 