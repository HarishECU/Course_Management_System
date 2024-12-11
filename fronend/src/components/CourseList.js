import React, { useEffect, useState } from 'react';
import './CourseList.css';
import { Link } from 'react-router-dom';


function CourseList() {
    const [courses, setCourses] = useState([]);
    const [userCourses, setUserCourses] = useState([]);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [filterStatus, setFilterStatus] = useState('All');
    const [sortOrder, setSortOrder] = useState('asc');
    const [currentPage, setCurrentPage] = useState(1);
    const coursesPerPage = 10;

    useEffect(() => {
        document.title = 'Courses';
        fetchCourses();
        fetchUserCourses();
    }, []);

    useEffect(() => {
        applyFiltersAndSorting();
    }, [searchQuery, filterStatus, sortOrder]);

    const fetchCourses = () => {
        fetch('http://localhost:5000/api/courses')
            .then(response => response.json())
            .then(data => setCourses(Array.isArray(data) ? data : []))
            .catch(error => {
                console.error('Error fetching courses:', error);
                setError('Error fetching courses.');
            });
    };

    const fetchUserCourses = () => {
        fetch('http://localhost:5000/api/user/courses', {
            method: 'GET',
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => setUserCourses(Array.isArray(data) ? data.map(course => course.id) : []))
        .catch(error => {
            console.error('Error fetching user courses:', error);
            setError('Error fetching user courses.');
        });
    };

    const enrollCourse = (courseId) => {
        fetch('http://localhost:5000/api/enroll', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ courseId })
        })
        .then(response => response.json())
        .then(data => {
            setMessage(data.message);
            if (data.success) {
                setUserCourses([...userCourses, courseId]);
            }
        })
        .catch(error => {
            console.error('Error enrolling in course:', error);
            setMessage('An error occurred while enrolling in the course.');
        });
    };

    const applyFiltersAndSorting = () => {
        let filteredCourses = [...courses];

        if (searchQuery) {
            filteredCourses = filteredCourses.filter(course =>
                course.title.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        if (filterStatus !== 'All') {
            filteredCourses = filteredCourses.filter(course =>
                course.status === filterStatus
            );
        }

        filteredCourses = filteredCourses.sort((a, b) => {
            if (sortOrder === 'asc') {
                return a.title.localeCompare(b.title);
            }
            return b.title.localeCompare(a.title);
        });

        return filteredCourses;
    };

    const handleSearchChange = (e) => {
        const query = e.target.value;
        setSearchQuery(query);
        if (query === '') {
            fetchCourses(); // Reset courses to all courses when search query is cleared
        }
    };

    const handleFilterChange = (e) => {
        setFilterStatus(e.target.value);
    };

    const handleSortChange = () => {
        setSortOrder(prevOrder => (prevOrder === 'asc' ? 'desc' : 'asc'));
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    const filteredCourses = applyFiltersAndSorting();
    const totalPages = Math.ceil(filteredCourses.length / coursesPerPage);
    const displayedCourses = filteredCourses.slice((currentPage - 1) * coursesPerPage, currentPage * coursesPerPage);

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="course-list">
            <h1>Course List</h1>

            <div className="controls">
                <input
                    type="text"
                    name="search"
                    placeholder="Search courses"
                    value={searchQuery}
                    onChange={handleSearchChange}
                />
            </div>

            {message && <p>{message}</p>}

            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {displayedCourses.map((course) => (
                        <tr key={course.id}>
                            <td><Link to={`/course/${course.id}`}>{course.title}</Link></td>
                            <td>{course.description}</td>
                            <td className='enroll'>
                                {userCourses.includes(course.id) ? (
                                    'Enrolled'
                                ) : (
                                    <button onClick={() => enrollCourse(course.id)}>Enroll</button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="pagination">
                <button className="prev" onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>Prev</button>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button
                        key={index + 1}
                        className={currentPage === index + 1 ? 'active' : ''}
                        onClick={() => handlePageChange(index + 1)}
                    >
                        {index + 1}
                    </button>
                ))}
                <button className="next" onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
            </div>

            <div className="course-count">
                {filteredCourses.length} courses found
            </div>

            <footer>
                <p>Footer content here</p>
            </footer>
        </div>
    );
}

export default CourseList;
