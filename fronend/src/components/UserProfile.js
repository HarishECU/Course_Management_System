import React, { useEffect, useState } from 'react';
import './UserProfile.css';

function UserProfile() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        document.title = 'Profile';
        fetch('http://localhost:5000/api/user/profile', {
            method: 'GET',
            credentials: 'include' // Include credentials to send session cookies
        })
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login'; // Redirect to login if unauthorized
                throw new Error('Unauthorized');
            }
            return response.json();
        })
        .then(data => setUser(data))
        .catch(error => setError(error.message));
    }, []);

    if (error) {
        return <p>{error}</p>;
    }

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div className="user-profile">
            <h1>User Profile</h1>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
            <p>Courses Enrolled: {user.courses ? user.courses.length : 0}</p>
        </div>
    );
}

export default UserProfile;
