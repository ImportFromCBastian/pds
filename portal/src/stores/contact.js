import axios from "axios";

const sendMessage = async (formData) => {
  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL
    const response = await axios.post(
      `${baseUrl}/messages/`, 
      formData, 
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response;
  } catch (error) {
    throw error.response;
  }
};

export { sendMessage };