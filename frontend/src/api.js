import axios from 'axios';

const API_URL = 'http://localhost:3001/generate'; // Adjust if running elsewhere

export const generateProductContent = async (data) => {
  const response = await axios.post(API_URL, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};
