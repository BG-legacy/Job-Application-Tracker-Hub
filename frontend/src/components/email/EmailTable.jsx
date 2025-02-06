import React, { useState } from 'react';
import '../../styles/email/EmailTable.css';
import PropTypes from 'prop-types';

const EmailTable = ({ 
    emails = [], 
    onSelect, 
    selectedEmails = [], 
    onEdit,
    editingId,
    setEditingId 
}) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(10);

    const emailsArray = Array.isArray(emails) ? emails : [];
    const totalPages = Math.ceil(emailsArray.length / itemsPerPage);

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentEmails = emailsArray.slice(indexOfFirstItem, indexOfLastItem);

    const isSelected = (messageId) => {
        return selectedEmails.some(email => email.message_id === messageId);
    };

    const renderCell = (email, field) => {
        switch (field) {
            case 'job_title':
                return (
                    <div className="job-title-cell">
                        <span className="title">{email.job_title || 'N/A'}</span>
                        {email.parsing_confidence > 0.8 && (
                            <span className="confidence-badge">✓</span>
                        )}
                    </div>
                );
            case 'company_name':
                return (
                    <div className="company-cell">
                        <span>{email.company_name || 'N/A'}</span>
                        {email.from_email && (
                            <span className="email-domain">
                                {email.from_email.split('@')[1]}
                            </span>
                        )}
                    </div>
                );
            case 'date':
                const dateValue = email.received_date || email.date;
                if (!dateValue) return 'N/A';
                
                try {
                    const date = new Date(dateValue);
                    if (isNaN(date.getTime())) return 'Invalid Date';
                    
                    const today = new Date();
                    const diffDays = Math.floor((today - date) / (1000 * 60 * 60 * 24));
                    
                    return (
                        <div className="date-cell">
                            <span>{date.toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric'
                            })}</span>
                            <span className="days-ago">
                                {diffDays === 0 ? 'Today' : 
                                 diffDays === 1 ? 'Yesterday' : 
                                 `${diffDays} days ago`}
                            </span>
                        </div>
                    );
                } catch (error) {
                    return 'Invalid Date';
                }
            case 'status':
                return (
                    <span className={`status-badge ${email.application_status || 'unknown'}`}>
                        {email.application_status || 'unknown'}
                    </span>
                );
            default:
                return 'N/A';
        }
    };

    return (
        <div className="email-table-container">
            {emailsArray.length === 0 ? (
                <div className="no-emails-message">
                    No job applications found. Try refreshing or adjusting your search criteria.
                </div>
            ) : (
                <table className="email-table">
                    <thead>
                        <tr>
                            <th>Job Title</th>
                            <th>Company</th>
                            <th>Applied</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentEmails.map((email) => (
                            <tr 
                                key={email.message_id || Math.random()}
                                className={isSelected(email.message_id) ? 'selected' : ''}
                            >
                                <td>{renderCell(email, 'job_title')}</td>
                                <td>{renderCell(email, 'company_name')}</td>
                                <td>{renderCell(email, 'date')}</td>
                                <td>{renderCell(email, 'status')}</td>
                                <td>
                                    <button 
                                        className={`select-btn ${isSelected(email.message_id) ? 'selected' : ''}`}
                                        onClick={() => onSelect(email)}
                                    >
                                        {isSelected(email.message_id) ? 'Deselect' : 'Select'}
                                    </button>
                                    <button 
                                        className="edit-btn"
                                        onClick={() => setEditingId(editingId === email.message_id ? null : email.message_id)}
                                    >
                                        {editingId === email.message_id ? 'Done' : 'Edit'}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>
                    <span>
                        Page {currentPage} of {totalPages}
                    </span>
                    <button
                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                        disabled={currentPage === totalPages}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
};

// Add PropTypes for better type checking
EmailTable.propTypes = {
    emails: PropTypes.array,
    onSelect: PropTypes.func.isRequired,
    selectedEmails: PropTypes.array,
    onEdit: PropTypes.func,
    editingId: PropTypes.string,
    setEditingId: PropTypes.func
};

export default EmailTable; 
