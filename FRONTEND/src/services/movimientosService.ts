import axios from "axios";
import type { Movimientos } from "../types";

export async function getMovimientos(
  url = "http://localhost:8001/api/movimientos"
) {
  try {
    const response = await axios.get<Movimientos>(url, {
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.log("Status:", error.response?.status);
      console.log("Mensaje del servidor:", error.response?.data?.message);
    }
    console.error("Error al obtener movimientos:", error);
    return {
      count: 0,
      next: "",
      previous: "",
      results: [],
    };
  }
}
