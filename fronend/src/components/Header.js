import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
    const [user, setUser] = useState(null);
    const [error, setError] = useState('');
    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                setUser(parsedUser);
            } catch (error) {
                console.error('Error parsing user data:', error);
            }
        }
    }, []);

    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('user');
        fetch('http://localhost:5000/api/logout', {
            method: 'POST',
            credentials: 'include' // Include credentials to send session cookies
        })
        .then(response => {
            if (response.status === 401) {
                window.location.href = '/login'; // Redirect to login if unauthorized
                throw new Error('Unauthorized');
            }
            return response.json();
        })
        .catch(error => setError(error.message));
        setUser(null);
        window.location.href = '/login'; // Redirect to login page
    };

    return (
        <header>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/courses">Courses</Link>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/profile">Profile</Link>
                {user ? (
                    <>
                        <span>Welcome, {user.name}</span>
                        <button onClick={handleLogout}>Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login">Login</Link>
                        <Link to="/register">Register</Link>
                    </>
                )}
            </nav>
        </header>
    );
}

export default Header;
