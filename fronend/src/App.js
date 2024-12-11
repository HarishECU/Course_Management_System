import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseList from './components/CourseList';
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import EnrollmentList from './components/EnrollmentList';
import CourseDetails from './components/CourseDetails';
import Login from './pages/Login';
import Register from './pages/Register';
import HomePage from './pages/HomePage';
import ErrorBoundary from './components/ErrorBoundary';
import './styles/App.css';

function App() {
    return (
        <Router>
            <Header />
            <ErrorBoundary>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/courses" element={<CourseList />} />
                    <Route path="/course/:id" element={<CourseDetails />} />
                    <Route path="/profile" element={<UserProfile />} />
                    <Route path="/enrollments" element={<EnrollmentList />} />
                </Routes>
            </ErrorBoundary>
            <Footer />
        </Router>
    );
}

export default App;
