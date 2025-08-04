import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import authApi from '../utils/authApi';
import { saveToken } from '../utils/auth';
import { useNavigate } from 'react-router-dom';

const GoogleLoginButton = () => {
  const navigate = useNavigate();

  const handleGoogleLogin = async (credentialResponse) => {
    try {
      const decoded = jwtDecode(credentialResponse.credential);
      const res = await authApi.post('/google-login', {
        email: decoded.email,
        name: decoded.name,
      });
      saveToken(res.data.token);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data?.error) {
        alert(`Google login failed: ${err.response.data.error}`);
      } else {
        alert('Google login failed');
      }
      console.error(err);
    }
  };

  return (
    <GoogleLogin
      onSuccess={handleGoogleLogin}
      onError={() => alert('Google login failed')}
    />
  );
};

export default GoogleLoginButton;
