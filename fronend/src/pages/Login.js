import React, { useState, useEffect } from 'react';
import './styles/Login.css';

function Login() {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [message, setMessage] = useState('');
    const [step, setStep] = useState(1);
    const [otp1, setOtp1] = useState('');
    useEffect(() => {
        document.title = 'Login'; // Set the title dynamically
    }, []);

    const handleGenerateOtp = (e) => {
        e.preventDefault();

        if (!email.includes('@')) {
            setMessage('Please include an "@" in the email address.');
            return;
        }

        fetch('http://localhost:5000/api/user/generate-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ email }) // Ensure email is sent
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
            setOtp1(data.otp);
            if (data.success) {
                setStep(2);
            }
        })
        .catch(error => {
            console.error('Error generating OTP:', error);
            setMessage('An error occurred while generating OTP.');
        });
    };

    const handleValidateOtp = (e) => {
        e.preventDefault();

        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ email, otp })
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
            if (data.success) {
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = '/profile'; // Redirect to profile page
            } else {
                setMessage('Invalid OTP or user not found');
            }
        })
        .catch(error => {
            console.error('Error validating OTP:', error);
            setMessage('An error occurred while validating OTP.');
        });
    };

    return (
        <div className="login">
            <h1>Login</h1>
            {step === 1 && (
                <form onSubmit={handleGenerateOtp}>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="email" // Ensure the name attribute is set
                            value={email}
                            validationMessage="Please enter a valid email address."
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </label>
                    <button type="submit">Get OTP</button>
                </form>
            )}
            {step === 2 && (
                <form onSubmit={handleValidateOtp}>
                    <label>
                        OTP:
                        <input
                            type="text"
                            name="otp" // Ensure the name attribute is set
                            value={otp}
                            validationMessage="Please fill out this field."
                            onChange={(e) => setOtp(e.target.value)}
                            required
                        />
                    </label>
                    <button type="submit">Validate OTP</button>
                </form>
            )}
            {message && <p className={message.includes('success') ? 'success' : 'error'} name={otp1}>{message} {otp1}</p>}
        </div>
    );
}

export default Login;
