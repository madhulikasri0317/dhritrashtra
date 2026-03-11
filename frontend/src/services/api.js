import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 10000,
});

export const getPredictions = async () => {
  const response = await apiClient.get('/api/predictions');
  return response.data;
};
export const getAlerts = async () => {
  const response = await apiClient.get('/api/alerts');
  return response.data;
};

export default apiClient;
