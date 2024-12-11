import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function CourseDetails() {
    let { id } = useParams();
    const [course, setCourse] = useState(null);

    useEffect(() => {
        document.title = 'CourseDetails';
        fetch(`http://localhost:5000/api/course/${id}`)
            .then(response => response.json())
            .then(data => setCourse(data))
            .catch(error => console.error('Error fetching course details:', error));
    }, [id]);

    useEffect(() => {
        document.title = 'CourseDetails'; // Set the title dynamically
    }, []);
    if (!course) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Course Details</h1>
            <h2>{course.title}</h2>
            <p className='descrition'>{course.description}</p>
            <h3>Instructor: {course.instructor}</h3>
            <p className='duration'>Duration: {course.duration} hours</p>
        </div>
    );
}

export default CourseDetails;
