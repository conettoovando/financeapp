// src/routes/PublicRoute.tsx
import { Navigate, Outlet } from "react-router";
import { useAuth } from "../context/useAuth";

const PublicRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <div>Cargando...</div>;

  return isAuthenticated ? <Navigate to="/dashboard" /> : <Outlet />;
};

export default PublicRoute;
