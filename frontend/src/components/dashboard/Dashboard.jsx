import React from 'react';
import { Link } from 'react-router-dom';
import DashboardSummary from './DashboardSummary';
import '../../styles/dashboard/Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard">
            <main className="dashboard-content">
                <DashboardSummary />
                
                <div className="dashboard-cards">
                    <div className="dashboard-card">
                        <h2>My Applications</h2>
                        <p>View and manage your job applications</p>
                        <Link to="/applications" className="card-link">
                            View Applications
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
