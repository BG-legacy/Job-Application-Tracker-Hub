import React, { useState, useEffect, useRef } from 'react';
import { userService } from '../../services/userService';
import { applicationService } from '../../services/applicationService';
import defaultAvatar from '../../assets/default-avatar.svg';
import '../../styles/users/UserProfile.css';
import { formatDate } from '../../utils/dateUtils';

const AVATAR_OPTIONS = [
    '/avatars/professional-1.svg',
    '/avatars/professional-2.svg',
    '/avatars/professional-3.svg',
    '/avatars/professional-4.svg',
    // Add more default avatar options
];

const UserProfile = () => {
    const [profile, setProfile] = useState({
        teams: [],
        first_name: '',
        last_name: '',
        title: '',
        bio: '',
        location: '',
        linkedin_url: '',
        github_url: '',
        portfolio_url: '',
    });
    const [applications, setApplications] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [activeTab, setActiveTab] = useState('overview');
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        title: '',
        bio: '',
        location: '',
        linkedin_url: '',
        github_url: '',
        portfolio_url: '',
    });
    const [showAvatarModal, setShowAvatarModal] = useState(false);
    const [selectedAvatar, setSelectedAvatar] = useState(null);
    const [uploadedFile, setUploadedFile] = useState(null);
    const fileInputRef = useRef(null);
    const [previewImage, setPreviewImage] = useState(null);

    useEffect(() => {
        fetchProfile();
        fetchApplications();
    }, []);

    const fetchProfile = async () => {
        try {
            const data = await userService.getProfile();
            setProfile(data);
            setFormData({
                first_name: data.first_name || '',
                last_name: data.last_name || '',
                title: data.title || '',
                bio: data.bio || '',
                location: data.location || '',
                linkedin_url: data.linkedin_url || '',
                github_url: data.github_url || '',
                portfolio_url: data.portfolio_url || '',
            });
        } catch (error) {
            console.error('Error fetching profile:', error);
        }
    };

    const fetchApplications = async () => {
        try {
            const data = await applicationService.getApplications();
            setApplications(data);
        } catch (error) {
            console.error('Error fetching applications:', error);
        }
    };

    const handleUpdate = async (e) => {
        e.preventDefault();
        try {
            const updatedProfile = await userService.updateProfile(formData);
            setProfile(updatedProfile);
            setIsEditing(false);
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    };

    const handleAvatarClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setUploadedFile(reader.result);
                setSelectedAvatar(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleAvatarSave = async () => {
        try {
            let avatarData = new FormData();
            if (uploadedFile) {
                // Convert base64 to file if needed
                const response = await fetch(uploadedFile);
                const blob = await response.blob();
                avatarData.append('avatar', blob, 'avatar.jpg');
            } else if (selectedAvatar) {
                avatarData.append('avatar_url', selectedAvatar);
            }

            await userService.patchProfile(avatarData);
            setProfile(prev => ({ ...prev, avatar: selectedAvatar }));
            setShowAvatarModal(false);
        } catch (error) {
            console.error('Error updating avatar:', error);
        }
    };

    const handleImageChange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            // Preview the image
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreviewImage(reader.result);
            };
            reader.readAsDataURL(file);

            // Upload the image
            try {
                const formData = new FormData();
                formData.append('avatar', file);
                const response = await userService.updateAvatar(formData);
                setProfile(prev => ({
                    ...prev,
                    avatar: response.avatar_url
                }));
            } catch (error) {
                console.error('Error uploading avatar:', error);
            }
        }
    };

    if (!profile) return <div className="loading">Loading...</div>;

    return (
        <div className="profile-container">
            <div className="profile-header">
                <div className="profile-header-info">
                    <div className="profile-avatar-container">
                        <div className="profile-avatar-wrapper" onClick={handleAvatarClick}>
                            <img 
                                src={previewImage || profile.avatar || defaultAvatar} 
                                alt={`${profile.first_name}'s avatar`}
                                className="profile-avatar"
                            />
                            <div className="avatar-overlay">
                                <span>Change Photo</span>
                            </div>
                        </div>
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleImageChange}
                            accept="image/*"
                            style={{ display: 'none' }}
                        />
                    </div>
                    <h1>{profile.first_name} {profile.last_name}</h1>
                    <h2>{profile.title || 'Job Seeker'}</h2>
                    {profile.tagline && (
                        <div className="profile-tagline">
                            {profile.tagline}
                        </div>
                    )}
                    {profile.bio && (
                        <div className="profile-bio-preview">
                            {profile.bio.length > 150 
                                ? `${profile.bio.substring(0, 150)}...` 
                                : profile.bio}
                        </div>
                    )}
                    <div className="profile-stats">
                        <div className="stat">
                            <span className="stat-number">{applications?.length || 0}</span>
                            <span className="stat-label">Applications</span>
                        </div>
                        <div className="stat">
                            <span className="stat-number">{profile?.teams?.length || 0}</span>
                            <span className="stat-label">Teams</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="profile-nav">
                <button 
                    className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
                    onClick={() => setActiveTab('overview')}
                >
                    Overview
                </button>
                <button 
                    className={`nav-tab ${activeTab === 'applications' ? 'active' : ''}`}
                    onClick={() => setActiveTab('applications')}
                >
                    Applications
                </button>
                <button 
                    className={`nav-tab ${activeTab === 'teams' ? 'active' : ''}`}
                    onClick={() => setActiveTab('teams')}
                >
                    Teams
                </button>
            </div>

            <div className="profile-content">
                {isEditing ? (
                    <div className="edit-profile-form">
                        <form onSubmit={handleUpdate}>
                            <div className="form-grid">
                                <div className="form-group">
                                    <label>First Name</label>
                                    <input
                                        type="text"
                                        value={formData.first_name}
                                        onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Last Name</label>
                                    <input
                                        type="text"
                                        value={formData.last_name}
                                        onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Professional Title</label>
                                    <input
                                        type="text"
                                        value={formData.title}
                                        onChange={(e) => setFormData({...formData, title: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Location</label>
                                    <input
                                        type="text"
                                        value={formData.location}
                                        onChange={(e) => setFormData({...formData, location: e.target.value})}
                                    />
                                </div>
                            </div>
                            <div className="form-group full-width">
                                <label>Bio</label>
                                <textarea
                                    value={formData.bio}
                                    onChange={(e) => setFormData({...formData, bio: e.target.value})}
                                    rows="4"
                                />
                            </div>
                            <div className="social-links">
                                <div className="form-group">
                                    <label>LinkedIn URL</label>
                                    <input
                                        type="url"
                                        value={formData.linkedin_url}
                                        onChange={(e) => setFormData({...formData, linkedin_url: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>GitHub URL</label>
                                    <input
                                        type="url"
                                        value={formData.github_url}
                                        onChange={(e) => setFormData({...formData, github_url: e.target.value})}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Portfolio URL</label>
                                    <input
                                        type="url"
                                        value={formData.portfolio_url}
                                        onChange={(e) => setFormData({...formData, portfolio_url: e.target.value})}
                                    />
                                </div>
                            </div>
                            <div className="form-actions">
                                <button type="submit" className="save-btn">Save Changes</button>
                                <button type="button" className="cancel-btn" onClick={() => setIsEditing(false)}>
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                ) : (
                    <>
                        {activeTab === 'overview' && (
                            <div className="profile-overview">
                                <div className="about-section">
                                    <h3>About</h3>
                                    <p>{profile.bio || 'No bio added yet.'}</p>
                                </div>
                                <div className="social-section">
                                    <h3>Connect</h3>
                                    <div className="social-links">
                                        {profile.linkedin_url && (
                                            <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer">
                                                LinkedIn
                                            </a>
                                        )}
                                        {profile.github_url && (
                                            <a href={profile.github_url} target="_blank" rel="noopener noreferrer">
                                                GitHub
                                            </a>
                                        )}
                                        {profile.portfolio_url && (
                                            <a href={profile.portfolio_url} target="_blank" rel="noopener noreferrer">
                                                Portfolio
                                            </a>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'applications' && (
                            <div className="applications-section">
                                <h3>Job Applications</h3>
                                <div className="applications-grid">
                                    {applications?.map(app => (
                                        <div key={app.id} className="application-card">
                                            <h4>{app.company_name}</h4>
                                            <p className="job-title">{app.job_title}</p>
                                            <p className="status" data-status={app.status}>
                                                {app.status}
                                            </p>
                                            <div className="application-date">
                                                <span className="exact-date">
                                                    Applied on {formatDate(app.date_applied)}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                    {(!applications || applications.length === 0) && (
                                        <div className="no-applications">
                                            <p>No applications yet</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {activeTab === 'teams' && (
                            <div className="teams-section">
                                <div className="teams-header">
                                    <h3>My Teams</h3>
                                    <button className="join-team-btn">
                                        <i className="fas fa-plus"></i> Join Team
                                    </button>
                                </div>
                                <div className="teams-grid">
                                    {profile?.teams?.map(team => (
                                        <div key={team.id} className="team-card">
                                            <div className="team-card-header">
                                                <img 
                                                    src={team.avatar || '/default-team-avatar.svg'} 
                                                    alt={team.name}
                                                    className="team-avatar"
                                                />
                                                <div className="team-info">
                                                    <h4>{team.name}</h4>
                                                    <span className="team-role">{team.role}</span>
                                                </div>
                                            </div>
                                            <div className="team-card-body">
                                                <p className="team-description">{team.description}</p>
                                                <div className="team-stats">
                                                    <div className="stat">
                                                        <i className="fas fa-users"></i>
                                                        <span>{team.member_count} members</span>
                                                    </div>
                                                    <div className="stat">
                                                        <i className="fas fa-calendar"></i>
                                                        <span>Joined {new Date(team.joined_at).toLocaleDateString()}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="team-card-footer">
                                                <button className="view-team-btn">View Team</button>
                                                <button className="team-menu-btn">
                                                    <i className="fas fa-ellipsis-v"></i>
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>

            {showAvatarModal && (
                <>
                    <div className="modal-overlay" onClick={() => setShowAvatarModal(false)} />
                    <div className="avatar-upload-modal">
                        <h3>Choose Your Avatar</h3>
                        <div className="avatar-options">
                            {AVATAR_OPTIONS.map((avatar, index) => (
                                <img
                                    key={index}
                                    src={avatar}
                                    alt={`Avatar option ${index + 1}`}
                                    className={`avatar-option ${selectedAvatar === avatar ? 'selected' : ''}`}
                                    onClick={() => setSelectedAvatar(avatar)}
                                />
                            ))}
                        </div>
                        <div className="upload-section">
                            <label className="upload-button">
                                Upload Custom Photo
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleFileUpload}
                                    style={{ display: 'none' }}
                                />
                            </label>
                        </div>
                        <div className="modal-actions">
                            <button 
                                className="modal-button cancel-button"
                                onClick={() => setShowAvatarModal(false)}
                            >
                                Cancel
                            </button>
                            <button 
                                className="modal-button save-button"
                                onClick={handleAvatarSave}
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default UserProfile; 