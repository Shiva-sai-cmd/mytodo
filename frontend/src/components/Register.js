import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authApi from '../utils/authApi';
import '../index.css';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await authApi.post('/register', { name, email, password });
      alert('Registered successfully! Please login.');
      navigate('/login');
    } catch (err) {
      alert(err?.response?.data?.error || 'Registration failed');
    }
  };

  return (
    <div className="form-page">
      <div className="animated-box">
        <div className="inner-box">
          <h3 className="form-title">Register</h3>
          <form onSubmit={handleRegister} className="register-form">
            <input
              type="text"
              placeholder="Full Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" className="submit-btn">Sign Up</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
