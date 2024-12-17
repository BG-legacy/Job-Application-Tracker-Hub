import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/dashboard/Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>Job Application Tracker</h1>
                <nav className="dashboard-nav">
                    <Link to="/applications" className="nav-link">My Applications</Link>
                    <button onClick={() => {
                        localStorage.removeItem('token');
                        window.location.href = '/login';
                    }} className="logout-button">
                        Logout
                    </button>
                </nav>
            </header>

            <main className="dashboard-content">
                <div className="dashboard-cards">
                    <div className="dashboard-card">
                        <h2>Applications</h2>
                        <p>Track and manage your job applications</p>
                        <Link to="/applications" className="card-link">
                            View Applications
                        </Link>
                    </div>

                    <div className="dashboard-card">
                        <h2>Quick Add</h2>
                        <p>Add a new job application</p>
                        <Link to="/applications/new" className="card-link">
                            Add Application
                        </Link>
                    </div>

                    <div className="dashboard-card">
                        <h2>AI Insights</h2>
                        <p>View AI-powered insights about your applications</p>
                        <Link to="/insights" className="card-link">
                            View Insights
                        </Link>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
