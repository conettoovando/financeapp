// src/api/financeApi.ts
import axios from "axios";
import authApi from "./authApi";

const financeApi = axios.create({
  baseURL: "http://localhost:8001/api",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    error ? prom.reject(error) : prom.resolve(token);
  });
  failedQueue = [];
};

financeApi.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => financeApi(originalRequest));
      }

      isRefreshing = true;

      try {
        // 👇 Aquí hacemos el refresh en la API de autenticación
        await authApi.post(
          "/auth/refresh-token",
          {},
          { withCredentials: true }
        );

        processQueue(null);
        return financeApi(originalRequest); // 🔁 Reintenta
      } catch (err) {
        processQueue(err, null);
        // ❌ Si no se puede refrescar, cerrar sesión
        window.location.href = "/login";
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default financeApi;
