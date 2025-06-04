import { type User } from "./user";

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: {
    email: string;
    password: string;
  }) => Promise<LoginResponse>;
  logout: () => Promise<void>;
  registerAcc: (credentials: {
    email: string;
    password: string;
    confirmpassword: string;
  }) => Promise<RegisterResponse>;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  fetchUser: () => Promise<void>;
}

type LoginResponse = void | { success: false; error?: string; status?: number };

type RegisterResponse = {
  success: string | boolean;
  error: string | null;
};
