import React, { useEffect, useState } from 'react';
import './EnrollmentList.css';

function EnrollmentList() {
    const [enrollments, setEnrollments] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/api/enrollments')
            .then(response => response.json())
            .then(data => setEnrollments(data))
            .catch(error => console.error('Error fetching enrollments:', error));
    }, []);

    return (
        <div className="enrollment-list">
            <h1>Enrollment List</h1>
            <ul>
                {enrollments.map((enrollment) => (
                    <li key={enrollment.id}>
                        <p>User ID: {enrollment.user_id}</p>
                        <p>Course ID: {enrollment.course_id}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EnrollmentList;
