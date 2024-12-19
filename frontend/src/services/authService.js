import api from './api';

export const authService = {
    async login(email, password) {
        try {
            const response = await api.post('/users/login/', { email, password });
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
            const response = await api.post('/users/signup/', userData);
            if (response.data.token) {
                localStorage.setItem('token', response.data.token);
                return response.data;
            }
            throw new Error('Registration successful but no token received');
        } catch (error) {
            if (error.response?.data) {
                const errorMessage = Object.entries(error.response.data)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join('\n');
                throw new Error(errorMessage);
            }
            throw new Error('Registration failed');
        }
    },

    async verifyToken() {
        try {
            await api.get('/users/verify/');
            return true;
        } catch (error) {
            return false;
        }
    },

    logout() {
        localStorage.removeItem('token');
    }
};