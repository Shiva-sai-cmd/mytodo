import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import authApi from '../utils/authApi';
import { saveToken } from '../utils/auth';
import GoogleLoginButton from './GoogleLoginButton';
import '../index.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await authApi.post('/login', { email, password });
      saveToken(res.data.token);
      navigate('/dashboard');
    } catch (err) {
      alert(err?.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="form-page">
      <div className="animated-box">
        <div className="inner-box">
          <h3 className="form-title">Login</h3>
          <form onSubmit={handleLogin} className="register-form">
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
            <button type="submit" className="submit-btn">Login</button>
          </form>

          <div className="text-center mt-3">
            <p style={{ color: '#ccc' }}>Or login with Google</p>
            <GoogleLoginButton />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
