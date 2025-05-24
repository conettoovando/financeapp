import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import axios from "axios";
import { useNavigate } from "react-router";

type User = {
  sub: string;
  email: string;
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
};

type MeResponse = {
  msg: string;
  user: User;
};

type LoginResponse = void | { success: false; error?: string; status?: number };

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoaging] = useState(true);
  const navigate = useNavigate();

  const fetchUser = async () => {
    try {
      const res = await axios.get<MeResponse>("http://localhost:8001/auth/me", {
        withCredentials: true,
      });
      setUser(res.data.user);
    } catch (err) {
      setUser(null);
    } finally {
      setIsLoaging(false);
    }
  };

  const login = async (credentials: {
    email: string;
    password: string;
  }): Promise<LoginResponse> => {
    try {
      await axios.post("http://localhost:8001/auth/login", credentials, {
        withCredentials: true,
      });
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

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }
  return context;
};
