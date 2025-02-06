import React, { useState, useEffect, useRef } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import api from '../../services/api';
import ApplicationModal from './ApplicationModal';
import ApplicationFilters from './ApplicationFilters';

const ApplicationList = () => {
    const [applications, setApplications] = useState([]);
    const [selectedApplication, setSelectedApplication] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [searchParams] = useSearchParams();
    const [currentDate, setCurrentDate] = useState(new Date());
    const [isSearchPanelOpen, setIsSearchPanelOpen] = useState(false);
    const searchPanelRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (searchPanelRef.current && !searchPanelRef.current.contains(event.target)) {
                setIsSearchPanelOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const fetchApplications = async (params) => {
        try {
            const queryString = params.toString();
            const response = await api.get(`applications/${queryString ? `?${queryString}` : ''}`);
            setApplications(response.data);
        } catch (error) {
            console.error('Error fetching applications:', error);
        }
    };

    useEffect(() => {
        fetchApplications(searchParams);
    }, [searchParams]);

    const handleFilterChange = (newParams) => {
        fetchApplications(newParams);
    };

    const getDaysInMonth = (date) => {
        return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    };

    const getFirstDayOfMonth = (date) => {
        return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    };

    const getMonthName = (date) => {
        return new Intl.DateTimeFormat('en-US', { month: 'long' }).format(date);
    };

    const getApplicationsForDate = (date) => {
        return applications.filter(app => {
            if (!app.date_applied) return false;
            
            const appDate = new Date(app.date_applied + 'T00:00:00Z');
            const compareDate = new Date(Date.UTC(
                currentDate.getFullYear(),
                currentDate.getMonth(),
                date
            ));
            
            return appDate.getUTCDate() === compareDate.getUTCDate() &&
                   appDate.getUTCMonth() === compareDate.getUTCMonth() &&
                   appDate.getUTCFullYear() === compareDate.getUTCFullYear();
        });
    };

    const handlePrevMonth = () => {
        setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
    };

    const handleNextMonth = () => {
        setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
    };

    const renderCalendar = () => {
        const daysInMonth = getDaysInMonth(currentDate);
        const firstDay = getFirstDayOfMonth(currentDate);
        const days = [];

        // Add empty cells for days before the first day of the month
        for (let i = 0; i < firstDay; i++) {
            days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
        }

        // Add cells for each day of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dayApplications = getApplicationsForDate(day);
            days.push(
                <div key={day} className="calendar-day">
                    <div className="day-number">{day}</div>
                    <div className="day-applications">
                        {dayApplications.map(app => (
                            <div 
                                key={app.id}
                                className={`application-tag status-${app.status.toLowerCase()}`}
                                onClick={() => {
                                    setSelectedApplication(app);
                                    setIsModalOpen(true);
                                }}
                            >
                                {app.company_name} - {app.job_title}
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        return days;
    };

    return (
        <div className="applications-container">
            <div className={`search-panel ${isSearchPanelOpen ? 'open' : ''}`} ref={searchPanelRef}>
                <div className="search-panel-content">
                    <h3>Search Applications</h3>
                    <ApplicationFilters onFilterChange={handleFilterChange} />
                </div>
            </div>

            <div className="calendar-controls">
                <div className="calendar-header">
                    <button className="month-nav" onClick={handlePrevMonth}>{"<"}</button>
                    <h2>{getMonthName(currentDate)} {currentDate.getFullYear()}</h2>
                    <button className="month-nav" onClick={handleNextMonth}>{">"}</button>
                </div>
                <div className="action-buttons">
                    <Link to="/applications/new" className="add-button">
                        Add New Application
                    </Link>
                    <button 
                        className="search-button"
                        onClick={() => setIsSearchPanelOpen(!isSearchPanelOpen)}
                    >
                        Search Applications
                    </button>
                </div>
            </div>
            <div className="calendar-grid">
                <div className="weekday-header">Sun</div>
                <div className="weekday-header">Mon</div>
                <div className="weekday-header">Tue</div>
                <div className="weekday-header">Wed</div>
                <div className="weekday-header">Thu</div>
                <div className="weekday-header">Fri</div>
                <div className="weekday-header">Sat</div>
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