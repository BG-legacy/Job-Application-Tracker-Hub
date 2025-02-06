import React, { useState, useEffect } from 'react';
import { aiInsightService } from '../../services/aiInsightService';
import { CircularProgress, Paper, Typography, Grid, Box } from '@mui/material';
import { 
    TrendingUp, 
    Assessment, 
    Timeline, 
    ShowChart 
} from '@mui/icons-material';

const MetricCard = ({ title, value, icon }) => (
    <Paper 
        elevation={0}
        sx={{
            p: 2.5,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            border: '1px solid',
            borderColor: 'rgba(0, 0, 0, 0.08)',
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
                transform: 'translateY(-2px)',
                borderColor: 'primary.light',
                boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
            }
        }}
    >
        <Box sx={{ color: 'primary.main', mb: 1, opacity: 0.9 }}>
            {icon}
        </Box>
        <Typography 
            variant="h6" 
            color="text.secondary" 
            gutterBottom 
            sx={{ fontSize: '0.875rem' }}
        >
            {title}
        </Typography>
        <Typography 
            variant="h4" 
            component="div" 
            sx={{ 
                fontWeight: 500,
                fontSize: '1.75rem',
                color: 'text.primary'
            }}
        >
            {value}%
        </Typography>
    </Paper>
);

const AIRecommendations = () => {
    const [insights, setInsights] = useState({
        chatgpt_analysis: '',
        metrics: {
            response_rate: 0,
            interview_rate: 0,
            success_rate: 0,
            market_alignment: 0
        }
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchInsights();
    }, []);

    const fetchInsights = async () => {
        try {
            const response = await aiInsightService.getRecommendations();
            setInsights({
                chatgpt_analysis: response.data.chatgpt_analysis || 'No analysis available',
                metrics: {
                    response_rate: response.data.metrics?.response_rate || 0,
                    interview_rate: response.data.metrics?.interview_rate || 0,
                    success_rate: response.data.metrics?.success_rate || 0,
                    market_alignment: response.data.metrics?.market_alignment || 0
                }
            });
        } catch (err) {
            setError('Failed to fetch AI recommendations');
        } finally {
            setLoading(false);
        }
    };

    const formatMetric = (value) => {
        return typeof value === 'number' ? value.toFixed(1) : '0.0';
    };

    if (loading) return (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
        </Box>
    );

    if (error) return (
        <Box sx={{ p: 2 }}>
            <Typography color="error">{error}</Typography>
        </Box>
    );

    return (
        <Box sx={{ p: { xs: 2, sm: 3 } }}>
            <Typography 
                variant="h4" 
                gutterBottom 
                sx={{ 
                    mb: 4, 
                    fontSize: { xs: '1.5rem', sm: '1.75rem' },
                    color: 'text.primary'
                }}
            >
                AI-Powered Insights
            </Typography>
            
            <Grid container spacing={2} sx={{ mb: 6 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <MetricCard 
                        title="Response Rate"
                        value={formatMetric(insights.metrics.response_rate)}
                        icon={<TrendingUp fontSize="large" />}
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <MetricCard 
                        title="Interview Rate"
                        value={formatMetric(insights.metrics.interview_rate)}
                        icon={<Assessment fontSize="large" />}
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <MetricCard 
                        title="Success Rate"
                        value={formatMetric(insights.metrics.success_rate)}
                        icon={<Timeline fontSize="large" />}
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <MetricCard 
                        title="Market Alignment"
                        value={formatMetric(insights.metrics.market_alignment)}
                        icon={<ShowChart fontSize="large" />}
                    />
                </Grid>
            </Grid>

            <Box sx={{ 
                width: '100%', 
                height: '1px', 
                bgcolor: 'rgba(0, 0, 0, 0.08)', 
                mb: 6
            }} />

            <Paper 
                elevation={0}
                sx={{ 
                    p: 3,
                    border: '1px solid',
                    borderColor: 'rgba(0, 0, 0, 0.08)',
                    maxWidth: '900px',
                    mx: 'auto',
                    height: 'auto',
                    mb: 4
                }}
            >
                <Typography 
                    variant="h5" 
                    gutterBottom 
                    sx={{ 
                        mb: 2, 
                        color: 'text.primary',
                        fontSize: '1.1rem'
                    }}
                >
                    AI Recommendation
                </Typography>
                <Typography 
                    variant="body1" 
                    sx={{ 
                        whiteSpace: 'pre-line',
                        lineHeight: 1.7,
                        color: 'text.secondary',
                        fontSize: '0.875rem',
                        overflow: 'visible',
                        textOverflow: 'clip'
                    }}
                >
                    {insights.chatgpt_analysis}
                </Typography>
            </Paper>
        </Box>
    );
};

export default AIRecommendations; 