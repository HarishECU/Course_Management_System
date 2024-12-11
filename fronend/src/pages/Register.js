import React, { useState, useEffect} from 'react';
import './styles/Register.css';

function Register() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    useEffect(() => {
        document.title = 'Register'; // Set the title dynamically
    }, []);
    const handleRegister = (e) => {
        e.preventDefault();

        fetch('http://localhost:5000/api/user/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email })
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
            if (data.success) {
                setName('');
                setEmail('');
            }
        })
        .catch(error => {
            console.error('Error registering user:', error);
            setMessage('An error occurred while registering.');
        });
    };

    return (
        <div className="register">
            <h1>Register</h1>
            <form onSubmit={handleRegister}>
                <label>
                    Name:
                    <input
                        type="text"
                        name='name'
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        
                    />
                </label>
                <label>
                    Email:
                    <input
                        type="email"
                        name='email'
                        value={email}
                        validationMessage="Please enter a valid email address."
                        onChange={(e) => setEmail(e.target.value)}
                        
                    />
                </label>
                <button type="submit">Register</button>
            </form>
            {message && <p className={message.includes('success') ? 'success' : 'error'}>{message} </p>}
        </div>
    );
}

export default Register;
