import { useEffect } from "react";
import { useNavigate } from "react-router";
import { useAuth } from "../context/useAuth";
import type { User } from "../types";

export function useRedirectIfAuthenticated(
  redirectTo: string = "/dashboard"
): User | null {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate(redirectTo);
    }
  }, [user, navigate, redirectTo]);

  return user;
}
