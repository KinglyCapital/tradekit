const API_BASE_URL = 'http://localhost:8000';

export const useFetch = async (endpoint: string, params: Record<string, any> = {}) => {
  const queryString = new URLSearchParams(params).toString();
  const url = `${API_BASE_URL}/${endpoint}${queryString ? `?${queryString}` : ''}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
};
