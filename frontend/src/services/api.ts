import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorDetails = error.response?.data || error.message;
    console.error('API request failure:', errorDetails);
    return Promise.reject(errorDetails);
  }
);

export default apiClient;
