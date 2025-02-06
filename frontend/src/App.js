import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from './theme';
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
import TeamsDashboard from './components/teams/TeamsDashboard';
import TeamDetails from './components/teams/TeamDetails';
import DataExchangePanel from './components/data/DataExchangePanel';
import EmailIntegration from './components/email/EmailIntegration';
import EmailSyncView from './components/email/EmailSyncView';
import './App.css';
import { AuthProvider } from './contexts/AuthContext';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <AuthProvider>
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
                                <Route
                                    path="/teams"
                                    element={
                                        <ProtectedRoute>
                                            <Navigation />
                                            <TeamsDashboard />
                                        </ProtectedRoute>
                                    }
                                />
                                <Route
                                    path="/teams/:teamId"
                                    element={
                                        <ProtectedRoute>
                                            <Navigation />
                                            <TeamDetails />
                                        </ProtectedRoute>
                                    }
                                />
                                <Route
                                    path="/data"
                                    element={
                                        <ProtectedRoute>
                                            <Navigation />
                                            <DataExchangePanel />
                                        </ProtectedRoute>
                                    }
                                />
                                <Route
                                    path="/email-integration"
                                    element={
                                        <ProtectedRoute>
                                            <Navigation />
                                            <EmailIntegration />
                                        </ProtectedRoute>
                                    }
                                />
                                <Route
                                    path="/applications/email-sync"
                                    element={
                                        <ProtectedRoute>
                                            <Navigation />
                                            <EmailSyncView />
                                        </ProtectedRoute>
                                    }
                                />
                            </Routes>
                        </div>
                    </div>
                </Router>
            </AuthProvider>
        </ThemeProvider>
    );
}

export default App;