import { Outlet, Link } from "react-router";

export default function RootLayout() {
  return (
    <div>
      <nav>
        <Link to="/">Inicio</Link> | <Link to="/login">Login</Link>
      </nav>
      <hr />
      <Outlet /> {/* AQUI SE RENDERIZAN RUTAS HIJAS */}
    </div>
  );
}
