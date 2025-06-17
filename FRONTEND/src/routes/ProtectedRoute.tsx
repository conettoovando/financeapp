import { Navigate, Outlet, useLocation } from "react-router";
import { useAuth } from "../context/useAuth";

export default function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) return <div>Cargando...</div>;

  return isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to={"/login"} state={{ from: location }} replace />
  );
}
