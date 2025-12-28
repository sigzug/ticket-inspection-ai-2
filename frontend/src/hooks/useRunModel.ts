import useSWRMutation from "swr/mutation";
import axios from "axios";
import type { UseModelRequest, UseModelResponse } from "../interfaces";
import { getCsrfToken } from "./useCsrf";

const defaultBaseUrl = (import.meta as any)?.env?.VITE_API_BASE_URL || "http://localhost:8000";

// Factory so we can access baseUrl inside the mutation fetcher
function createAxiosPoster(baseUrl: string) {
  return async function axiosPoster(
    url: string,
    { arg }: { arg: UseModelRequest },
  ): Promise<UseModelResponse> {
    const payload = {
      ...arg,
      // Ensure ISO string for the backend
      departure_time: new Date(arg.departure_time as any).toISOString(),
    };

    // Ensure CSRF token (sets cookie if missing)
    const csrfToken = await getCsrfToken(baseUrl);

    const res = await axios.post<UseModelResponse>(url, payload, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "X-CSRFToken": csrfToken,
      },
    });
    return res.data;
  };
}

/**
 * useRunModel
 * - runModel: call to trigger the POST
 * - data: latest response
 * - error: error from last mutation
 * - isMutating: loading state
 * - reset: clear cached mutation data/error
 */
export function useRunModel(baseUrl: string = defaultBaseUrl) {
  const url = `${baseUrl.replace(/\/$/, "")}/api/run_model/`;
  const poster = createAxiosPoster(baseUrl);
  const { trigger, data, error, isMutating, reset } = useSWRMutation<
    UseModelResponse,
    any,
    string,
    UseModelRequest
  >(url, poster);

  return {
    runModel: trigger,
    data,
    error,
    isMutating,
    reset,
  };
}
