import { useEffect, useState, type ReactNode } from "react";
import axios from "axios";
import { useNavigate } from "react-router";
import { AuthContext } from "./AuthContext";
import type {
  User,
  MeResponse,
  LoginResponse,
  RegisterResponse,
} from "../types";

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const fetchUser = async () => {
    if (document.cookie.includes("token_type")) {
      try {
        const res = await axios.get<MeResponse>("http://localhost:8000/me", {
          withCredentials: true,
        });
        setUser(res.data.user);
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          // Token expirado: intento refrescar
          try {
            await axios.post(
              "http://localhost:8000/refresh",
              {},
              {
                withCredentials: true,
              }
            );

            // Si refresca con éxito, intento nuevamente obtener el usuario
            const res = await axios.get<MeResponse>(
              "http://localhost:8000/me",
              {
                withCredentials: true,
              }
            );
            setUser(res.data.user);
            return;
          } catch {
            // Refresh falló, limpiar sesión
            setUser(null);
          }
        } else {
          // Otros errores
          setUser(null);
        }
      } finally {
        setIsLoading(false);
      }
    } else {
      setUser(null);
      setIsLoading(false);
    }
  };

  const login = async (credentials: {
    email: string;
    password: string;
  }): Promise<LoginResponse> => {
    try {
      const response = await axios.post(
        "http://localhost:8000/login",
        credentials,
        {
          withCredentials: true,
        }
      );
      if (response.status === 200) {
        await axios.post(
          "http://localhost:8001/auth/login",
          { user_id: response.data.id },
          { withCredentials: true }
        );
      }
      await fetchUser();
      navigate("/dashboard");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        return {
          success: false,
          error: error.response?.data.detail,
          status: error.response?.status,
        };
      }
      return {
        success: false,
        error: "Error desconocido",
      };
    }
  };

  const registerAcc = async (credentials: {
    email: string;
    password: string;
    confirmpassword: string;
  }): Promise<RegisterResponse> => {
    if (credentials.password !== credentials.confirmpassword) {
      return {
        success: false,
        error: "Las contraseñas no coinciden",
      };
    }
    try {
      const response = await axios.post(
        "http://localhost:8000/register",
        credentials,
        {
          withCredentials: true,
        }
      );
      if (response.status === 201) {
        navigate("/login");
        return {
          success: true,
          error: null,
        };
      } else {
        return {
          success: false,
          error: "Error en el registro",
        };
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        return {
          success: false,
          error: error.response?.data.detail || "Error en el registro",
        };
      }
      return {
        success: false,
        error: "Error desconocido",
      };
    }
  };

  const logout = async () => {
    await axios.post(
      "http://localhost:8001/auth/logout",
      {},
      { withCredentials: true }
    );
    setUser(null);
    navigate("/");
  };

  useEffect(() => {
    fetchUser();
  }, []);

  if (isLoading) {
    return <div>Cargando sesión...</div>;
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        registerAcc,
        logout,
        setUser,
        fetchUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
