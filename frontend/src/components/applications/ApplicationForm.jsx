import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const ApplicationForm = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        company_name: '',
        position: '',
        job_title: '',
        job_description: '',
        notes: '',
        status: 'Pending',
        date_applied: new Date().toISOString().split('T')[0]
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('applications/', formData);
            navigate('/applications');
        } catch (error) {
            console.error('Error creating application:', error.response?.data || error);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="application-form">
            <div className="form-group">
                <label>Company Name *</label>
                <input
                    type="text"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Position *</label>
                <input
                    type="text"
                    name="position"
                    value={formData.position}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Job Title *</label>
                <input
                    type="text"
                    name="job_title"
                    value={formData.job_title}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Job Description (Optional)</label>
                <textarea
                    name="job_description"
                    value={formData.job_description}
                    onChange={handleChange}
                    placeholder="Enter job description..."
                />
            </div>
            <div className="form-group">
                <label>Notes (Optional)</label>
                <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    placeholder="Add any notes..."
                />
            </div>
            <div className="form-group">
                <label>Status *</label>
                <select name="status" value={formData.status} onChange={handleChange}>
                    <option value="Pending">Pending</option>
                    <option value="Applied">Applied</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Accepted">Accepted</option>
                    <option value="Withdrawn">Withdrawn</option>
                </select>
            </div>
            <div className="form-group">
                <label>Applied Date *</label>
                <input
                    type="date"
                    name="date_applied"
                    value={formData.date_applied}
                    onChange={handleChange}
                    required
                />
            </div>
            <button type="submit">Submit Application</button>
        </form>
    );
};

export default ApplicationForm; 