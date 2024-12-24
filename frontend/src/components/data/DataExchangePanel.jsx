import React, { useState } from 'react';
import api from '../../services/api';
import '../../styles/data/DataExchangePanel.css';

const DataExchangePanel = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState('');

    const handleFileSelect = (event) => {
        setSelectedFile(event.target.files[0]);
        setError(null);
        setSuccessMessage('');
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select a file to upload');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        setUploading(true);
        setError(null);

        try {
            await api.post('/data/import/excel/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSuccessMessage('File uploaded and processed successfully!');
            setSelectedFile(null);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to upload file');
        } finally {
            setUploading(false);
        }
    };

    const handleDownload = async () => {
        try {
            const response = await api.get('/data/export/excel/', {
                responseType: 'blob'
            });
            
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `applications_export_${new Date().toISOString().slice(0,10)}.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            setError('Failed to download file');
        }
    };

    return (
        <div className="data-exchange-panel">
            <h2>Import/Export Applications</h2>
            
            <div className="upload-section">
                <h3>Import from Excel</h3>
                <div className="file-input-wrapper">
                    <input
                        type="file"
                        accept=".xlsx,.xls"
                        onChange={handleFileSelect}
                        id="file-upload"
                    />
                    <label htmlFor="file-upload" className="file-input-label">
                        {selectedFile ? selectedFile.name : 'Choose Excel File'}
                    </label>
                </div>
                <button 
                    onClick={handleUpload}
                    disabled={!selectedFile || uploading}
                    className="upload-button"
                >
                    {uploading ? 'Uploading...' : 'Upload'}
                </button>
            </div>

            <div className="download-section">
                <h3>Export to Excel</h3>
                <button 
                    onClick={handleDownload}
                    className="download-button"
                >
                    Download Applications
                </button>
            </div>

            {error && <div className="error-message">{error}</div>}
            {successMessage && <div className="success-message">{successMessage}</div>}
        </div>
    );
};

export default DataExchangePanel; 