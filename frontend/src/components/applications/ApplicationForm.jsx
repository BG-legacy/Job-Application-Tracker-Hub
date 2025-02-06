import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/applications/ApplicationForm.css';
import { STATUS_CHOICES } from '../../constants/applicationConstants';

const ApplicationForm = () => {
    const navigate = useNavigate();
    const today = new Date().toISOString().split('T')[0]; // Format: YYYY-MM-DD

    const [formData, setFormData] = useState({
        company_name: '',
        position: '',
        job_title: '',
        job_description: '',
        notes: '',
        status: 'Pending',
        date_applied: today
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await api.post('/applications/', formData);
            navigate('/applications');
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to submit application');
            setLoading(false);
        }
    };

    return (
        <div className="application-form-container">
            <h2>New Application</h2>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="company_name">Company Name</label>
                    <input
                        type="text"
                        id="company_name"
                        name="company_name"
                        value={formData.company_name}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="position">Position</label>
                    <input
                        type="text"
                        id="position"
                        name="position"
                        value={formData.position}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="job_title">Job Title</label>
                    <input
                        type="text"
                        id="job_title"
                        name="job_title"
                        value={formData.job_title}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="status">Status</label>
                    <select
                        id="status"
                        name="status"
                        value={formData.status}
                        onChange={handleChange}
                        required
                    >
                        {STATUS_CHOICES.map(status => (
                            <option key={status} value={status}>
                                {status}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="date_applied">Date Applied</label>
                    <input
                        type="date"
                        id="date_applied"
                        name="date_applied"
                        value={formData.date_applied}
                        onChange={handleChange}
                        max={today}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="job_description">Job Description</label>
                    <textarea
                        id="job_description"
                        name="job_description"
                        value={formData.job_description}
                        onChange={handleChange}
                        rows="4"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="notes">Notes</label>
                    <textarea
                        id="notes"
                        name="notes"
                        value={formData.notes}
                        onChange={handleChange}
                        rows="4"
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Submit Application'}
                </button>
            </form>
        </div>
    );
};

export default ApplicationForm; 