import { useState, useCallback } from 'react';
import apiClient from '../services/api';

export function useApi<T = any>() {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const request = useCallback(async (
    method: 'get' | 'post' | 'put' | 'delete',
    url: string,
    body?: any,
    headers?: any
  ) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient({
        method,
        url,
        data: body,
        headers,
      });
      setData(response.data);
      return response.data;
    } catch (err: any) {
      const errMsg = err?.message || 'Something went wrong';
      setError(errMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    data,
    loading,
    error,
    request,
  };
}
