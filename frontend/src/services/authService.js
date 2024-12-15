
import api from './api';

export const authService = {
    async login(email, password) {
        try {
            const response = await api.post('users/login/', { email, password });
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                return response.data;
            }
        } catch (error) {
            throw error.response?.data || { message: 'Login failed' };
        }
    },

    async register(userData) {
        try {
            const response = await api.post('users/register/', userData);
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                return response.data;
            }
        } catch (error) {
            throw error.response?.data || { message: 'Registration failed' };
        }
    },

    logout() {
        localStorage.removeItem('token');
    }
};