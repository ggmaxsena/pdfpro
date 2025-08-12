// frontend/app/diarias/hooks/useDiariasApi.js
import useSWR from 'swr';
import {
  getTravelRequests,
  getTravelRequest,
  createTravelRequest,
  updateTravelRequest,
  deleteTravelRequest,
  calculateDiarias
} from '../lib/api';

// Hook to fetch all travel requests
export const useGetTravelRequests = () => {
  const { data, error, mutate } = useSWR('/api/travel/travel-requests/', getTravelRequests);

  return {
    travelRequests: data,
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
};

// Hook to fetch a single travel request
export const useGetTravelRequest = (id) => {
  const { data, error, mutate } = useSWR(id ? `/api/travel/travel-requests/${id}/` : null, () => getTravelRequest(id));

  return {
    travelRequest: data,
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
};

// Hook for creating a travel request
export const useCreateTravelRequest = () => {
  return async (data) => {
    return await createTravelRequest(data);
  };
};

// Hook for updating a travel request
export const useUpdateTravelRequest = () => {
  return async (id, data) => {
    return await updateTravelRequest(id, data);
  };
};

// Hook for deleting a travel request
export const useDeleteTravelRequest = () => {
  return async (id) => {
    return await deleteTravelRequest(id);
  };
};

// Hook for calculating diarias
export const useCalculateDiarias = () => {
    return async (data) => {
        return await calculateDiarias(data);
    };
};
