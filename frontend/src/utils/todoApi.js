import axios from 'axios';
import { getToken } from './auth';

const todoApi = axios.create({
  baseURL: 'https://mytodo-q9zx.onrender.com/api/todo',
});

todoApi.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default todoApi;
