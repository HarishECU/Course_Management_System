import React, { useState } from 'react';
import './styles/Login.css';

function Login() {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [message, setMessage] = useState('');
    const [step, setStep] = useState(1);

    const handleGenerateOtp = (e) => {
        e.preventDefault();

        fetch('/api/user/generate-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
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

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, otp })
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
            if (data.success) {
                // Redirect or perform further actions upon successful OTP validation
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
                            value={email}
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
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            required
                        />
                    </label>
                    <button type="submit">Validate OTP</button>
                </form>
            )}
            {message && <p>{message}</p>}
        </div>
    );
}

export default Login;
