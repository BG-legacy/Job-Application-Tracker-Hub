import React, { useState } from 'react';
import api from '../../services/api';

const AvatarUpload = ({ onAvatarUpdate }) => {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('avatar', file);

        setUploading(true);
        setError(null);

        try {
            const response = await api.put('/users/profile/avatar/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            onAvatarUpdate(response.data.avatar);
        } catch (err) {
            setError('Failed to upload avatar. Please try again.');
            console.error('Avatar upload error:', err);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="avatar-upload">
            <input
                type="file"
                accept="image/jpeg,image/png,image/svg+xml"
                onChange={handleFileChange}
                disabled={uploading}
            />
            {uploading && <p>Uploading...</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default AvatarUpload; 