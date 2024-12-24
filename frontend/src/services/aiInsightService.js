import api from './api';

export const aiInsightService = {
    // Get general AI insights
    getInsights() {
        return api.get('/ai-insights/');
    },

    // Get insights for a specific application
    getApplicationInsights(applicationId) {
        return api.get(`/ai-insights/application/${applicationId}/`);
    },

    // Get dashboard summary with AI metrics
    getDashboardSummary() {
        return api.get('/ai-insights/dashboard/summary/');
    },

    // Get AI recommendations
    getRecommendations() {
        return api.get('/ai-insights/recommendations/');
    }
}; 