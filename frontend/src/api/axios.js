import axios from 'axios'

const apiClient = axios.create({
  // BURASI ÇOK ÖNEMLİ: Kendi bilgisayarındaki Django portunu yaz (Genelde 8000)
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token') || localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});