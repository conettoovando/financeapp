import { isAxiosError } from "axios";
import type { Movimientos } from "../types";
import financeApi from "../api/financeApi";

export async function getMovimientos(url = "/movimientos") {
  try {
    const response = await financeApi.get<Movimientos>(url);
    return response.data;
  } catch (error) {
    if (isAxiosError(error)) {
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
