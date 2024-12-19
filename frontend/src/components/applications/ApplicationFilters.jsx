import React from 'react';
import { useSearchParams } from 'react-router-dom';

const ApplicationFilters = ({ onFilterChange }) => {
    const [searchParams, setSearchParams] = useSearchParams();
    
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        const newParams = new URLSearchParams(searchParams);
        
        if (value) {
            newParams.set(name, value);
        } else {
            newParams.delete(name);
        }
        
        setSearchParams(newParams);
        onFilterChange(newParams);
    };

    return (
        <div className="filter-container">
            <div className="filter-group">
                <label>Search</label>
                <input
                    type="text"
                    name="search"
                    placeholder="Search applications..."
                    value={searchParams.get('search') || ''}
                    onChange={handleFilterChange}
                    className="search-input"
                />
            </div>

            <div className="filter-group">
                <label>Status</label>
                <select
                    name="status"
                    value={searchParams.get('status') || ''}
                    onChange={handleFilterChange}
                    className="filter-select"
                >
                    <option value="">All Statuses</option>
                    <option value="Pending">Pending</option>
                    <option value="Interview">Interview</option>
                    <option value="Offer">Offer</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Accepted">Accepted</option>
                    <option value="Withdrawn">Withdrawn</option>
                </select>
            </div>

            <div className="filter-group">
                <label>Date Range</label>
                <div className="date-range">
                    <input
                        type="date"
                        name="date_applied_after"
                        value={searchParams.get('date_applied_after') || ''}
                        onChange={handleFilterChange}
                        className="date-input"
                    />
                    <span>to</span>
                    <input
                        type="date"
                        name="date_applied_before"
                        value={searchParams.get('date_applied_before') || ''}
                        onChange={handleFilterChange}
                        className="date-input"
                    />
                </div>
            </div>
        </div>
    );
};

export default ApplicationFilters; 