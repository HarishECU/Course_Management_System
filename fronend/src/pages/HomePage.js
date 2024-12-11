import React from 'react';
import './styles/HomePage.css';
import { useEffect, useState } from 'react';

function HomePage() {
    useEffect(() => {
        document.title = 'Home';
    });
    return (
        <div className="homepage">
            <h1>Welcome to the LMS Application</h1>
            <p>Your gateway to a world of learning!</p>
        </div>
    );
}

export default HomePage;
