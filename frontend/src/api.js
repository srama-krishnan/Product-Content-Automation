import axios from 'axios';

const API_URL = 'http://localhost:5000/generate';  // or 'http://127.0.0.1:5000/generate'

export const generateProductContent = async (data) => {
  const response = await axios.post(API_URL, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};
