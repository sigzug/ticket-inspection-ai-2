import useSWR from "swr";
import axios from "axios";
import type { CategoriesResponse } from "../interfaces.ts";

export interface Categories {
  only_standing: string[];
  checked: string[];
  wagon: string[];
  notes: string[];
  line: string[];
  departure_station: string[];
  arrival_station: string[];
}

const defaultBaseUrl = (import.meta as any)?.env?.VITE_API_BASE_URL || "http://localhost:8000";

const axiosFetcher = async (url: string): Promise<CategoriesResponse> => {
  const res = await axios.get<CategoriesResponse>(url, {
    withCredentials: true,
    headers: { Accept: "application/json" },
  });
  return res.data;
};

export function useCategories(baseUrl: string = defaultBaseUrl) {
  const url = `${baseUrl.replace(/\/$/, "")}/api/categories/`;
  const { data, error, isLoading, mutate } = useSWR<CategoriesResponse>(url, axiosFetcher);

  return {
    categories: data?.categories,
    isLoading,
    isError: !!error,
    error,
    mutate,
  };
}
