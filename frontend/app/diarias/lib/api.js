// frontend/app/diarias/lib/api.js

const API_BASE_URL = '/api/travel';

// Helper to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(errorData.message || 'An error occurred');
  }
  return response.json();
};

// Function to get the JWT token (you might need to adjust where you store it)
const getAuthToken = () => {
  return localStorage.getItem('token');
};

const getHeaders = () => {
  const headers = {
    'Content-Type': 'application/json',
  };
  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const getTravelRequests = async () => {
  const response = await fetch(`${API_BASE_URL}/travel-requests/`, {
    headers: getHeaders(),
  });
  return handleResponse(response);
};

export const getTravelRequest = async (id) => {
  const response = await fetch(`${API_BASE_URL}/travel-requests/${id}/`, {
    headers: getHeaders(),
  });
  return handleResponse(response);
};

export const createTravelRequest = async (data) => {
  const response = await fetch(`${API_BASE_URL}/travel-requests/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(response);
};

export const updateTravelRequest = async (id, data) => {
  const response = await fetch(`${API_BASE_URL}/travel-requests/${id}/`, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse(response);
};

export const deleteTravelRequest = async (id) => {
  const response = await fetch(`${API_BSE_URL}/travel-requests/${id}/`, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  if (response.status !== 204) {
    return handleResponse(response);
  }
  return { success: true };
};

export const calculateDiarias = async (data) => {
    const response = await fetch(`${API_BASE_URL}/diarias/calculate`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify(data),
    });
    return handleResponse(response);
}
