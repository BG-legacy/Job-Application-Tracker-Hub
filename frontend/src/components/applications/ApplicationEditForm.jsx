import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/applications/ApplicationForm.css';

const ApplicationEditForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        company_name: '',
        position: '',
        job_title: '',
        date_applied: '',
        status: 'Pending',
        job_description: '',
        notes: ''
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchApplication = useCallback(async () => {
        try {
            const response = await api.get(`/applications/${id}/`);
            setFormData(response.data);
            setLoading(false);
        } catch (err) {
            setError('Failed to fetch application details');
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        fetchApplication();
    }, [fetchApplication]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.put(`/applications/${id}/`, formData);
            navigate('/applications');
        } catch (err) {
            setError('Failed to update application');
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="form-container">
            <h2>Edit Application</h2>
            <form onSubmit={handleSubmit} className="application-form">
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
                    <label htmlFor="date_applied">Date Applied</label>
                    <input
                        type="date"
                        id="date_applied"
                        name="date_applied"
                        value={formData.date_applied}
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
                        <option value="Pending">Pending</option>
                        <option value="Interview">Interview</option>
                        <option value="Offer">Offer</option>
                        <option value="Rejected">Rejected</option>
                        <option value="Accepted">Accepted</option>
                        <option value="Withdrawn">Withdrawn</option>
                    </select>
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

                <div className="form-actions">
                    <button type="submit" className="submit-btn">Update Application</button>
                    <button 
                        type="button" 
                        className="cancel-btn"
                        onClick={() => navigate('/applications')}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ApplicationEditForm;