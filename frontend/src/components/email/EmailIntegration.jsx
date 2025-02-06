import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/email/EmailIntegration.css';

const EmailIntegration = () => {
    const [connectionStatus, setConnectionStatus] = useState('disconnected');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const checkConnectionStatus = async () => {
        try {
            const response = await api.get('/email/connection-status/');
            console.log('Connection status response:', response.data); // Debug log
            setConnectionStatus(response.data.is_connected ? 'connected' : 'disconnected');
        } catch (err) {
            console.error('Error checking email connection status:', err);
            setError('Failed to check connection status');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        // Check URL parameters for OAuth callback status
        const params = new URLSearchParams(window.location.search);
        const status = params.get('status');
        const error = params.get('error');

        if (status === 'success') {
            console.log('OAuth callback success detected'); // Debug log
            setConnectionStatus('connected');
            // Clear the URL parameters
            window.history.replaceState({}, '', window.location.pathname);
        } else if (error) {
            setError(decodeURIComponent(error));
            // Clear the URL parameters
            window.history.replaceState({}, '', window.location.pathname);
        }

        // Always check the connection status
        checkConnectionStatus();
    }, []);

    const handleConnect = async () => {
        try {
            setLoading(true);
            const response = await api.post('/email/connect-email/');
            
            if (response.data.auth_url) {
                // Redirect to Google OAuth consent screen
                window.location.href = response.data.auth_url;
            }
        } catch (err) {
            console.error('Error initiating email connection:', err);
            setError('Failed to connect email account');
            setLoading(false);
        }
    };

    const handleDisconnect = async () => {
        try {
            setLoading(true);
            await api.post('/email/disconnect/');
            setConnectionStatus('disconnected');
        } catch (err) {
            console.error('Error disconnecting email:', err);
            setError('Failed to disconnect email account');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="email-integration loading">Loading...</div>;
    }

    return (
        <div className="email-integration">
            <h2>Email Integration</h2>
            
            {error && (
                <div className="error-message">
                    {error}
                    <button onClick={() => setError(null)}>Dismiss</button>
                </div>
            )}

            <div className="connection-status">
                <h3>Connection Status</h3>
                <p className={`status ${connectionStatus}`}>
                    {connectionStatus === 'connected' ? 'Connected' : 'Not Connected'}
                </p>
            </div>

            <div className="integration-actions">
                {connectionStatus === 'connected' ? (
                    <>
                        <button 
                            className="disconnect-button"
                            onClick={handleDisconnect}
                            disabled={loading}
                        >
                            Disconnect Email
                        </button>
                        <button 
                            className="sync-button"
                            onClick={() => navigate('/applications/email-sync')}
                        >
                            Sync Job Applications
                        </button>
                    </>
                ) : (
                    <button 
                        className="connect-button"
                        onClick={handleConnect}
                        disabled={loading}
                    >
                        Connect Gmail Account
                    </button>
                )}
            </div>

            <div className="integration-info">
                <h3>About Email Integration</h3>
                <p>
                    Connect your Gmail account to automatically track job applications 
                    from your email. We'll scan for job-related emails and help you 
                    organize your job search.
                </p>
                <div className="permissions-info">
                    <h4>Required Permissions:</h4>
                    <ul>
                        <li>Read-only access to your Gmail messages</li>
                        <li>Limited to job-related emails only</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default EmailIntegration; 