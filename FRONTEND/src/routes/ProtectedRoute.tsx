import { Navigate } from "react-router";
import { useAuth } from "../context/useAuth";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <div>Cargando...</div>;

  return isAuthenticated ? children : <Navigate to={"/login"} />;
};

export default ProtectedRoute;
