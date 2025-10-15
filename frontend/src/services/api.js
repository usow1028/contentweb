import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',
  withCredentials: true
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const loginRequest = async (credentials) => {
  const response = await api.post('login/', credentials);
  if (response.data.token) {
    localStorage.setItem('authToken', response.data.token);
  }
  return response.data;
};

export const logoutRequest = async () => {
  await api.post('logout/');
  localStorage.removeItem('authToken');
};

export const registerRequest = async (payload) => {
  return api.post('register/', payload);
};

export const fetchCurrentUser = async () => {
  const response = await api.get('me/');
  return response.data;
};

export const fetchSubmissions = async () => {
  const response = await api.get('submissions/');
  return response.data;
};

export const createSubmission = async (formData) => {
  return api.post('submissions/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const fetchSubmissionDetail = async (id) => {
  const response = await api.get(`submissions/${id}/`);
  return response.data;
};

export const voteSubmission = async (id, payload) => {
  const response = await api.post(`submissions/${id}/vote/`, payload);
  return response.data;
};

export const fetchWeeklyResults = async () => {
  const response = await api.get('results/weekly/');
  return response.data;
};

export default api;
