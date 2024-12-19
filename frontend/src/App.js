import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/common/Navigation';
import ProtectedRoute from './components/common/ProtectedRoute';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './components/dashboard/Dashboard';
import ApplicationList from './components/applications/ApplicationList';
import ApplicationForm from './components/applications/ApplicationForm';
import ApplicationEditForm from './components/applications/ApplicationEditForm';
import AIRecommendations from './components/insights/AIRecommendations';
import UserProfile from './components/users/UserProfile';
import './App.css';

function App() {
    return (
        <Router>
            <div className="App">
                <div className="content-wrapper">
                    <Routes>
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/applications"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <ApplicationList />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/applications/new"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <ApplicationForm />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/insights"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <AIRecommendations />
                                </ProtectedRoute>
                            }
                        />
                        <Route path="/login" element={<LoginForm />} />
                        <Route path="/register" element={<RegisterForm />} />
                        <Route path="/" element={<LoginForm />} />
                        <Route
                            path="/applications/:id/edit"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <ApplicationEditForm />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/profile"
                            element={
                                <ProtectedRoute>
                                    <Navigation />
                                    <UserProfile />
                                </ProtectedRoute>
                            }
                        />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;