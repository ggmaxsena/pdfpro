
const fetcher = async (url, options = {}) => {
  const baseUrl = 'http://localhost:8000/api';
  const fullUrl = `${baseUrl}${url}`;

  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    credentials: 'include', // Equivalente ao withCredentials: true do axios
  };

  const token = localStorage.getItem('auth_token');
  if (token) {
    defaultOptions.headers['Authorization'] = `Bearer ${token}`;
  }

  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  if (options.body) {
    mergedOptions.body = JSON.stringify(options.body);
  }

  const response = await fetch(fullUrl, mergedOptions);

  if (!response.ok) {
    const error = new Error('An error occurred while fetching the data.');
    try {
      error.info = await response.json();
    } catch (e) {
      error.info = { statusText: response.statusText };
    }
    error.status = response.status;
    throw error;
  }

  // Retorna null para respostas sem conteúdo (ex: 204 No Content)
  if (response.status === 204) {
    return null;
  }

  return response.json();
};

export default fetcher;
