import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import { Link } from 'react-router-dom';


function Dashboard() {
    const [courses, setCourses] = useState([]);
    const [error, setError] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [filteredCourses, setFilteredCourses] = useState([]);
    const [sortOrder, setSortOrder] = useState('asc');
    const [filterStatus, setFilterStatus] = useState('All');
    const [currentPage, setCurrentPage] = useState(1);
    const coursesPerPage = 5;

    useEffect(() => {
        document.title = 'Dashboard';
        fetchCourses();
    }, []);

    useEffect(() => {
        applyFilters();
    }, [courses, searchQuery, filterStatus, sortOrder]);

    const fetchCourses = () => {
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
        .then(data => setCourses(Array.isArray(data) ? data : []))
        .catch(error => setError(error.message));
    };

    const applyFilters = () => {
        let updatedCourses = courses;

        if (searchQuery) {
            updatedCourses = updatedCourses.filter(course =>
                course.title.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        if (filterStatus !== 'All') {
            updatedCourses = updatedCourses.filter(course =>
                course.status === filterStatus
            );
        }

        if (sortOrder === 'asc') {
            updatedCourses = updatedCourses.sort((a, b) => a.title.localeCompare(b.title));
        } else {
            updatedCourses = updatedCourses.sort((a, b) => b.title.localeCompare(a.title));
        }

        setFilteredCourses(updatedCourses);
    };

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
    };

    const handleFilterChange = (e) => {
        setFilterStatus(e.target.value);
    };

    const handleSortChange = () => {
        setSortOrder(prevOrder => (prevOrder === 'asc' ? 'desc' : 'asc'));
    };

    const handlePageChange = (direction) => {
        if (direction === 'next' && currentPage < totalPages) {
            setCurrentPage(currentPage + 1);
        } else if (direction === 'prev' && currentPage > 1) {
            setCurrentPage(currentPage - 1);
        }
    };

    const totalPages = Math.ceil(filteredCourses.length / coursesPerPage);
    const displayedCourses = filteredCourses.slice((currentPage - 1) * coursesPerPage, currentPage * coursesPerPage);

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <p>Welcome to your dashboard!</p>

            <div className="controls">
                <input
                    type="text"
                    name="search"
                    placeholder="Search courses"
                    value={searchQuery}
                    onChange={handleSearchChange}
                />
                <button className="sort" onClick={handleSortChange}>
                    Sort {sortOrder === 'asc' ? 'Descending' : 'Ascending'}
                </button>
                <select className="filter" value={filterStatus} onChange={handleFilterChange}>
                    <option value="All">All</option>
                    <option value="Active">Active</option>
                    <option value="Completed">Completed</option>
                </select>
                <button className="apply" onClick={applyFilters}>Apply Filters</button>
            </div>

            <h2>Your Courses</h2>
            <ul className="course-list">
                {displayedCourses.map(course => (
                    <li key={course.id}>
                        <h3><Link to={`/course/${course.id}`}>{course.title}</Link></h3>
                        <p>{course.description}</p>
                        <div className="progress-bar" value={course.progress}></div>
                    </li>
                ))}
            </ul>

            <div className="pagination">
                <button className="prev" onClick={() => handlePageChange('prev')} disabled={currentPage === 1}>Prev</button>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button
                        key={index + 1}
                        className={currentPage === index + 1 ? 'active' : ''}
                        onClick={() => setCurrentPage(index + 1)}
                    >
                        {index + 1}
                    </button>
                ))}
                <button className="next" onClick={() => handlePageChange('next')} disabled={currentPage === totalPages}>Next</button>
            </div>

            <div className="course-count">
                {filteredCourses.length} courses found
            </div>

            <div className="notifications">
                <div className="message">New course added</div>
            </div>

            <footer>
                <p>Footer content here</p>
            </footer>
        </div>
    );
}

export default Dashboard;
