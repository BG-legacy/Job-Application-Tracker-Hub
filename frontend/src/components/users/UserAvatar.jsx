import React from 'react';
import defaultAvatar from '../../assets/default-avatar.svg';

const UserAvatar = ({ avatarUrl, size = 'medium' }) => {
    const sizeClass = {
        small: 'w-8 h-8',
        medium: 'w-12 h-12',
        large: 'w-24 h-24'
    }[size];

    return (
        <img
            src={avatarUrl || defaultAvatar}
            alt="User avatar"
            className={`rounded-full object-cover ${sizeClass}`}
            onError={(e) => {
                e.target.src = defaultAvatar;
            }}
        />
    );
};

export default UserAvatar; 