import React, { useState, useEffect } from 'react';
import EmailTable from './EmailTable';
import api from '../../services/api';
import '../../styles/email/EmailSyncView.css';

const EmailSyncView = () => {
    const [parsedEmails, setParsedEmails] = useState([]);
    const [selectedEmails, setSelectedEmails] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [editingId, setEditingId] = useState(null);
    const [nextPageToken, setNextPageToken] = useState(null);
    const [hasMore, setHasMore] = useState(true);

    // Fetch emails when component mounts
    useEffect(() => {
        fetchEmails();
    }, []);

    const fetchEmails = async (pageToken = null) => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await api.post('/email/scrape-emails/', { 
                days_back: 30,
                page_token: pageToken 
            });
            
            // Ensure we have valid email data
            const newEmails = response.data.emails || [];
            
            if (pageToken) {
                // Append new emails to existing list
                setParsedEmails(prev => [...prev, ...newEmails]);
            } else {
                // Reset list for fresh fetch
                setParsedEmails(newEmails);
            }
            
            setNextPageToken(response.data.next_page_token);
            setHasMore(!!response.data.next_page_token);
            
        } catch (err) {
            console.error('Error fetching emails:', err);
            setError('Failed to fetch emails. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const loadMore = () => {
        if (nextPageToken && !loading) {
            fetchEmails(nextPageToken);
        }
    };

    const handleEmailEdit = (messageId, field, value) => {
        setParsedEmails(emails => 
            emails.map(email => 
                email.message_id === messageId 
                    ? { ...email, [field]: value }
                    : email
            )
        );
    };

    const handleSave = async () => {
        try {
            if (!selectedEmails.length) {
                setError('Please select at least one email to save');
                return;
            }

            setLoading(true);
            setError(null);

            // Only send the message IDs
            const email_ids = selectedEmails.map(email => email.message_id);
            
            const response = await api.post('/email/confirm-applications/', {
                email_ids: email_ids
            });

            if (response.data.saved_emails > 0) {
                // Clear selected emails and refresh the list
                setSelectedEmails([]);
                await fetchEmails();
            }

            return response.data;
        } catch (err) {
            console.error('Error saving applications:', err);
            setError(err.response?.data?.error || 'Failed to save applications');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    if (loading && parsedEmails.length === 0) {
        return <div className="email-sync-loading">Loading emails...</div>;
    }

    if (error) {
        return (
            <div className="email-sync-error">
                <p>{error}</p>
                <button onClick={fetchEmails}>Retry</button>
            </div>
        );
    }

    return (
        <div className="email-sync-view">
            <h2>Job Application Emails</h2>
            
            <div className="sync-controls">
                <button 
                    onClick={fetchEmails} 
                    disabled={loading}
                    className="refresh-btn"
                >
                    Refresh Emails
                </button>
                
                <button 
                    onClick={handleSave}
                    disabled={loading || selectedEmails.length === 0}
                    className="save-btn"
                >
                    Save Selected ({selectedEmails.length})
                </button>
            </div>

            <EmailTable 
                emails={parsedEmails}
                onSelect={email => {
                    setSelectedEmails(prev => {
                        const isSelected = prev.some(e => e.message_id === email.message_id);
                        return isSelected 
                            ? prev.filter(e => e.message_id !== email.message_id)
                            : [...prev, email];
                    });
                }}
                selectedEmails={selectedEmails}
                onEdit={handleEmailEdit}
                editingId={editingId}
                setEditingId={setEditingId}
            />
            
            {hasMore && (
                <button 
                    className="load-more-btn"
                    onClick={loadMore}
                    disabled={loading}
                >
                    {loading ? 'Loading...' : 'Load More Emails'}
                </button>
            )}
        </div>
    );
};

export default EmailSyncView; 
