import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const GENERATE_ENDPOINT = "/generate";  // route segment, not full URL
export const generateProductContent = async (data) => {
  const response = await axios.post(`${BASE_URL}${GENERATE_ENDPOINT}`, data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};
