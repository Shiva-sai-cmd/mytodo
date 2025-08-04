// src/utils/todoApi.js
import axios from 'axios';
import { getToken } from './auth';

const todoApi = axios.create({
  baseURL: 'http://localhost:5000/api/todo', // adjust if needed
});

// Attach token to every request
todoApi.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default todoApi;
