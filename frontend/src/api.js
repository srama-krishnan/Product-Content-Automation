import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const generateProductContent = async (data) => {
  const response = await axios.post(API_URL, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};
