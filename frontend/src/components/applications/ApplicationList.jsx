import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import ApplicationModal from './ApplicationModal';

const ApplicationList = () => {
    const [applications, setApplications] = useState([]);
    const [currentDate, setCurrentDate] = useState(new Date());
    const [selectedApplication, setSelectedApplication] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchApplications();
    }, []);

    const fetchApplications = async () => {
        try {
            const response = await api.get('applications/');
            setApplications(response.data);
        } catch (error) {
            console.error('Error fetching applications:', error);
        }
    };

    // Get days in month
    const getDaysInMonth = (date) => {
        return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    };

    // Get first day of month (0 = Sunday, 1 = Monday, etc.)
    const getFirstDayOfMonth = (date) => {
        return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    };

    // Group applications by date
    const getApplicationsByDate = (date) => {
        return applications.filter(app => {
            const appDate = new Date(app.date_applied);
            return appDate.getDate() === date &&
                   appDate.getMonth() === currentDate.getMonth() &&
                   appDate.getFullYear() === currentDate.getFullYear();
        });
    };

    // Navigate between months
    const changeMonth = (increment) => {
        setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + increment, 1));
    };

    const handleApplicationClick = (application) => {
        setSelectedApplication(application);
        setIsModalOpen(true);
    };

    // Generate calendar grid
    const renderCalendar = () => {
        const daysInMonth = getDaysInMonth(currentDate);
        const firstDayOfMonth = getFirstDayOfMonth(currentDate);
        const days = [];

        // Add empty cells for days before the first day of the month
        for (let i = 0; i < firstDayOfMonth; i++) {
            days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
        }

        // Add cells for each day of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const appsForDay = getApplicationsByDate(day);
            days.push(
                <div key={day} className="calendar-day">
                    <div className="day-number">{day}</div>
                    <div className="day-applications">
                        {appsForDay.map(app => (
                            <div 
                                key={app.id} 
                                className={`application-item status-${app.status.toLowerCase()}`}
                                onClick={() => handleApplicationClick(app)}
                            >
                                <span>{app.company_name} - {app.position}</span>
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        return days;
    };

    return (
        <div className="calendar-view">
            <div className="calendar-header">
                <button onClick={() => changeMonth(-1)}>&lt;</button>
                <h2>
                    {currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}
                </h2>
                <button onClick={() => changeMonth(1)}>&gt;</button>
            </div>
            <Link to="/applications/new" className="add-button">
                Add New Application
            </Link>
            <div className="calendar-grid">
                <div className="weekday">Sun</div>
                <div className="weekday">Mon</div>
                <div className="weekday">Tue</div>
                <div className="weekday">Wed</div>
                <div className="weekday">Thu</div>
                <div className="weekday">Fri</div>
                <div className="weekday">Sat</div>
                {renderCalendar()}
            </div>

            {isModalOpen && selectedApplication && (
                <ApplicationModal
                    application={selectedApplication}
                    onClose={() => setIsModalOpen(false)}
                />
            )}
        </div>
    );
};

export default ApplicationList; 