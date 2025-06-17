import { useEffect, useState, type ReactNode } from "react";
import { useNavigate, useLocation } from "react-router";
import { AuthContext } from "./AuthContext";
import { isAxiosError } from "axios";
import authApi from "../api/authApi";
import financeApi from "../api/financeApi";
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
  const location = useLocation();

  // 👉 Nunca hace navigate, solo carga el usuario si los tokens son válidos
  const fetchUser = async () => {
    if (document.cookie.includes("token_type")) {
      try {
        const res = await authApi.get<MeResponse>("/me");
        setUser(res.data.user);
      } catch (error) {
        if (isAxiosError(error) && error.response?.status === 401) {
          try {
            await authApi.post("/refresh");
            const res = await authApi.get<MeResponse>("/me");
            setUser(res.data.user);
          } catch {
            setUser(null); // refresh falló
          }
        } else {
          setUser(null); // otro error
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
      const response = await authApi.post("/login", credentials);

      if (response.status === 200) {
        await financeApi.post("/auth/login", { user_id: response.data.id });
      }

      await fetchUser(); // ya no navega aquí adentro

      // Solo login redirige a donde el usuario quería ir
      const from = location.state?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });

      return { success: true };
    } catch (error) {
      if (isAxiosError(error)) {
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
      const response = await authApi.post("/register", credentials);

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
      if (isAxiosError(error)) {
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
    await authApi.post("/logout", {});
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
