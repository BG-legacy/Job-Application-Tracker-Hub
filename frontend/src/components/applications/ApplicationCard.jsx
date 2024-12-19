import React from 'react';
import { formatDate } from '../../utils/dateUtils';

const ApplicationCard = ({ application }) => {
    const {
        company_name,
        position,
        status,
        date_applied
    } = application;

    return (
        <div className="application-card">
            <h3>{company_name}</h3>
            <p>{position}</p>
            <div className={`status-badge ${status.toLowerCase()}`}>
                {status}
            </div>
            <div className="application-date">
                {date_applied ? (
                    <span className="exact-date">Applied on {formatDate(date_applied)}</span>
                ) : (
                    <span className="no-date">Application date not specified</span>
                )}
            </div>
        </div>
    );
};

export default ApplicationCard; 