import { useRedirectIfAuthenticated } from "../hooks/useRedirectIfAuthenticated";

export default function Home() {
  useRedirectIfAuthenticated();

  return <h1>Bienvenido a la app</h1>;
}
