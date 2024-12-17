import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../../styles/common/Navigation.css';

const Navigation = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <nav className="main-nav">
            <div className="nav-brand">
                <Link to="/dashboard">Job Tracker</Link>
            </div>
            <div className="nav-links">
                <Link to="/applications">Applications</Link>
                <Link to="/insights">Insights</Link>
                <button onClick={handleLogout} className="logout-btn">
                    Logout
                </button>
            </div>
        </nav>
    );
};

export default Navigation; 