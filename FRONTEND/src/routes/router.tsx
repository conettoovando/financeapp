import { createBrowserRouter } from "react-router";
import RootLayout from "../layouts/RootLayout";
import PrivateLayout from "../layouts/PrivateLayout";
import NotFound from "../pages/NotFound";
import Home from "../pages/Home";
import Login from "../pages/Login";
import { AuthProvider } from "../context/AuthProvider";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import Dashboard from "../pages/dashboard";

const router = createBrowserRouter([
  // 🔓 Rutas públicas
  {
    path: "/",
    element: (
      <AuthProvider>
        <PublicRoute />
      </AuthProvider>
    ),
    errorElement: <NotFound />,
    children: [
      {
        path: "/",
        element: <RootLayout />,
        children: [
          { index: true, element: <Home /> },
          { path: "login", element: <Login /> },
        ],
      },
    ],
  },

  // 🔐 Rutas privadas
  {
    path: "/dashboard",
    element: (
      <AuthProvider>
        <ProtectedRoute>
          <PrivateLayout />
        </ProtectedRoute>
      </AuthProvider>
    ),
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "perfil",
        element: <div>Tu perfil</div>,
      },
    ],
  },
]);

export default router;
