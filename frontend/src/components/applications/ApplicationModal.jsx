import React from 'react';
import { Link } from 'react-router-dom';

const ApplicationModal = ({ application, onClose }) => {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{application.company_name}</h2>
                    <button className="close-button" onClick={onClose}>&times;</button>
                </div>
                <div className="modal-body">
                    <div className="detail-row">
                        <label>Position:</label>
                        <span>{application.position}</span>
                    </div>
                    <div className="detail-row">
                        <label>Job Title:</label>
                        <span>{application.job_title}</span>
                    </div>
                    <div className="detail-row">
                        <label>Status:</label>
                        <span className={`status-badge status-${application.status.toLowerCase()}`}>
                            {application.status}
                        </span>
                    </div>
                    <div className="detail-row">
                        <label>Applied Date:</label>
                        <span>{new Date(application.date_applied).toLocaleDateString()}</span>
                    </div>
                    {application.job_description && (
                        <div className="detail-section">
                            <label>Job Description:</label>
                            <p>{application.job_description}</p>
                        </div>
                    )}
                    {application.notes && (
                        <div className="detail-section">
                            <label>Notes:</label>
                            <p>{application.notes}</p>
                        </div>
                    )}
                </div>
                <div className="modal-footer">
                    <Link 
                        to={`/applications/${application.id}/edit`} 
                        className="edit-button"
                    >
                        Edit Application
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default ApplicationModal; 