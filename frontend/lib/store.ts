import { create } from "zustand";
import { persist } from "zustand/middleware";
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface User {
  id: number;
  email: string;
  full_name: string;
  role: "artist" | "venue" | "booker" | "admin";
  is_active: boolean;
  is_verified: boolean;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string, role: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const formData = new URLSearchParams();
          formData.append("username", email);
          formData.append("password", password);

          const response = await axios.post(`${API_URL}/auth/token`, formData, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
          });

          const { access_token } = response.data;
          localStorage.setItem("token", access_token);

          const userResponse = await axios.get(`${API_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${access_token}` },
          });

          set({ user: userResponse.data, token: access_token, isLoading: false });
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || "Login failed",
            isLoading: false,
          });
        }
      },

      register: async (email: string, password: string, fullName: string, role: string) => {
        set({ isLoading: true, error: null });
        try {
          await axios.post(`${API_URL}/auth/register`, {
            email,
            password,
            full_name: fullName,
            role,
          });

          await get().login(email, password);
        } catch (error: any) {
          set({
            error: error.response?.data?.detail || "Registration failed",
            isLoading: false,
          });
        }
      },

      logout: () => {
        localStorage.removeItem("token");
        set({ user: null, token: null });
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({ token: state.token }),
    }
  )
);

export const apiClient = axios.create({
  baseURL: API_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
