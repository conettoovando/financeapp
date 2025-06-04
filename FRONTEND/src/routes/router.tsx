import { createBrowserRouter } from "react-router";
import RootLayout from "../layouts/RootLayout";
import PrivateLayout from "../layouts/PrivateLayout";
import NotFound from "../pages/NotFound";
import Home from "../pages/Home";
import Login from "../pages/Dashboard/auth/Login";
import { AuthProvider } from "../context/AuthProvider";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import Dashboard from "../pages/Dashboard/Dashboard";
import VerCuenta from "../pages/Cuentas/VerCuenta";
import CrearCuenta from "../pages/Cuentas/CrearCuenta";
import Register from "../pages/Dashboard/auth/Register";

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
          { path: "register", element: <Register /> },
        ],
      },
    ],
  },

  // 🔐 Rutas privadas
  {
    path: "/tabs",
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
        path: "dashboard",
        element: <Dashboard />,
      },
      {
        path: "cuenta",
        children: [
          { index: true, element: <h1>Pagina principal de cuenta</h1> },
          { path: "add-cuenta", element: <CrearCuenta /> },
          { path: ":cuenta_id", element: <VerCuenta /> },
        ],
      },
    ],
  },
]);

export default router;
