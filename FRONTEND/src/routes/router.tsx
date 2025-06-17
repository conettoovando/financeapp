import { createBrowserRouter, Outlet } from "react-router";
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
import CrearMovimiento from "../pages/Movimientos/CrearMovimiento";

const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <AuthProvider>
        <Outlet /> {/* solo actúa como punto común para rutas hijas */}
      </AuthProvider>
    ),
    errorElement: <NotFound />,

    children: [
      // 🔓 Rutas públicas con layout RootLayout
      {
        element: <PublicRoute />, // Verifica si está autenticado
        children: [
          {
            element: <RootLayout />, // Navbar para login/register
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
        path: "tabs",
        element: <ProtectedRoute />, // Verifica si está logueado
        children: [
          {
            element: <PrivateLayout />, // Sidebar + outlet
            children: [
              { index: true, path: "dashboard", element: <Dashboard /> },
              {
                path: "cuenta",
                children: [
                  { index: true, element: <h1>Pagina principal de cuenta</h1> },
                  { path: "add-cuenta", element: <CrearCuenta /> },
                  { path: ":cuenta_id", element: <VerCuenta /> },
                ],
              },
              {
                path: "actions",
                children: [
                  { path: "crear-movimiento", element: <CrearMovimiento /> },
                ],
              },
            ],
          },
        ],
      },
    ],
  },
]);

export default router;
