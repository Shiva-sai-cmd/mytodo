import React from 'react';
import { Link } from 'react-router-dom';
import '../index.css';

const Home = () => {
  return (
    <div className="home-bg">
      <div className="home-overlay">
        <div className="home-content text-center">
          <h1 className="home-title">Welcome to <span>Todo Manager</span></h1>
          <p className="home-subtitle">Stay organized. Track your tasks efficiently.</p>
          <div className="home-buttons">
            <Link to="/login" className="btn btn-home btn-primary-home">Login</Link>
            <Link to="/register" className="btn btn-home btn-outline-home">Register</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
