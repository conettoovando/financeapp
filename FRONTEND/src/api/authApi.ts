// src/api/authApi.ts
import axios from "axios";

const authApi = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export default authApi;
