import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../../services/authService';
import UserAvatar from '../users/UserAvatar';
import api from '../../services/api';
import '../../styles/common/Navigation.css';

const Navigation = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
    const [userProfile, setUserProfile] = useState(null);

    useEffect(() => {
        fetchUserProfile();
    }, []);

    const fetchUserProfile = async () => {
        try {
            const response = await api.get('/users/profile/');
            setUserProfile(response.data);
        } catch (err) {
            console.error('Error fetching user profile:', err);
        }
    };

    const handleLogout = () => {
        authService.logout();
        navigate('/login');
    };

    return (
        <nav className="navigation">
            <div className="nav-container">
                <div className="nav-left">
                    <Link to="/dashboard" className="brand-logo">
                        <span>Job Tracker</span>
                    </Link>
                    <Link to="/applications" className={location.pathname === '/applications' ? 'active' : ''}>
                        Applications
                    </Link>
                    <Link to="/teams" className={location.pathname === '/teams' ? 'active' : ''}>
                        Teams
                    </Link>
                    <Link to="/insights" className={location.pathname === '/insights' ? 'active' : ''}>
                        Insights
                    </Link>
                    <Link 
                        to="/data" 
                        className={`nav-link ${location.pathname === '/data' ? 'active' : ''}`}
                    >
                        Import/Export
                    </Link>
                    <Link
                        to="/email-integration"
                        className={`nav-link ${location.pathname === '/email-integration' ? 'active' : ''}`}
                    >
                        Email Integration
                    </Link>
                </div>

                <div className="nav-right">
                    <div className="profile-menu">
                        <button 
                            className="profile-button"
                            onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                        >
                            <UserAvatar 
                                avatarUrl={userProfile?.avatar_url} 
                                size="small" 
                            />
                        </button>

                        {isProfileMenuOpen && (
                            <div className="dropdown-menu">
                                <Link to="/profile" className="dropdown-item">
                                    Profile Settings
                                </Link>
                                <button onClick={handleLogout} className="dropdown-item">
                                    Logout
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navigation; 