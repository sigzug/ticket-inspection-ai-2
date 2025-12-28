import axios from "axios";

const defaultBaseUrl =
  (import.meta as any)?.env?.VITE_API_BASE_URL || "http://localhost:8000";

function readCookie(name: string): string | null {
  const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return m ? decodeURIComponent(m[2]) : null;
}

/**
 * Ensures a CSRF token is available.
 * - Reads 'csrftoken' from cookies; if missing, calls /api/csrf/ to set it.
 * - Returns the token string to be used in the 'X-CSRFToken' header.
 */
export async function getCsrfToken(baseUrl: string = defaultBaseUrl): Promise<string> {
  const existing = readCookie("csrftoken");
  if (existing) return existing;

  const base = baseUrl.replace(/\/$/, "");
  const res = await axios.get<{ csrfToken: string }>(`${base}/api/csrf/`, {
    withCredentials: true,
    headers: { Accept: "application/json" },
  });

  // After this call, Django sets the csrftoken cookie; prefer cookie value
  const token = readCookie("csrftoken") || res.data?.csrfToken || "";
  if (!token) {
    throw new Error("Failed to obtain CSRF token");
  }
  return token;
}