import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/common/Navigation';
import ProtectedRoute from './components/common/ProtectedRoute';
import LoginForm from './components/auth/LoginForm';
import RegisterForm from './components/auth/RegisterForm';
import Dashboard from './components/dashboard/Dashboard';
import ApplicationList from './components/applications/ApplicationList';
import ApplicationForm from './components/applications/ApplicationForm';

function App() {
    return (
        <Router>
            <div className="app">
                <Routes>
                    <Route path="/login" element={<LoginForm />} />
                    <Route path="/register" element={<RegisterForm />} />
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
                        path="/applications/:id/edit"
                        element={
                            <ProtectedRoute>
                                <Navigation />
                                <ApplicationForm />
                            </ProtectedRoute>
                        }
                    />
                    <Route path="/" element={<LoginForm />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;