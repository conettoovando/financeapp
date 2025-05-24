import { useForm } from "react-hook-form";
import { useAuth } from "../context/AuthContext";

type formData = {
  email: string;
  password: string;
};

export default function Login() {
  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<formData>();

  const onSubmit = handleSubmit(async (data) => {
    try {
      const response = await login({
        email: data.email,
        password: data.password,
      });

      if (response && "error" in response) {
        alert(
          `Error ${response.status}: ${response.error || "Error desconocido"}`
        );
      } else {
        alert("Sesión iniciada correctamente");
      }
    } catch (error) {
      alert("Ocurrió un error inesperado");
    } finally {
      reset();
    }
  });

  return (
    <main className="container h-screen grid place-items-center mx-auto">
      <form
        className="flex flex-col gap-5 items-center border border-slate-700 rounded-md w-full max-w-md px-8 py-10"
        onSubmit={onSubmit}
      >
        <div className="space-y-4">
          <h1 className="text-2xl font-bold text-center">
            Únete a cuidar tus finanzas personales
          </h1>
          <p className="text-slate-500">
            Registrare para unirte y recibir las herramientas de control
            necesarias.
          </p>
        </div>

        <div className="space-y-3 w-full">
          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm text-slate-700 font-semibold"
            >
              Correo electronico:
            </label>

            <input
              type="email"
              id="email"
              className={`border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600`}
              placeholder="correo@dominio.com"
              {...register("email", {
                required: "El nombre de usuario es requerido",
              })}
            />
            {errors.email && (
              <p className="text-red-500 font-medium text-sn w-full">
                {errors.email.message}
              </p>
            )}
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm text-slate-700 font-semibold"
            >
              Contraseña{" "}
            </label>

            <input
              type="password"
              id="password"
              className={`border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600`}
              placeholder="******"
              {...register("password", {
                required: "Se requiere una contraseña",
              })}
            />
            {errors.password && (
              <p className="text-red-500 font-medium text-sn w-full">
                {errors.password.message}
              </p>
            )}
          </div>
        </div>

        <div className="flex gap-3 items-center w-full">
          <input
            type="checkbox"
            id="terms"
            className="accent-stone-800 cursor-pointer rounded-sm w-5 h-5"
          />
          <label
            htmlFor="terms"
            className="text-sm text-slate-700 font-semibold cursor-pointer leading-5"
          >
            He leído y acepto los{" "}
            <a href="#" className="text-blue-700 underline capitalize">
              Términos & conficiones
            </a>{" "}
            y la
            <a href="#" className="text-blue-700 underline">
              {" "}
              política de privacidad.
            </a>
          </label>
        </div>

        <div className="flex flex-col gap-3 w-full">
          <button
            type="submit"
            className="bg-stone-800 text-white py-3 rounded-md font-medium cursor-pointer"
          >
            Ingresar
          </button>
          <button
            type="button"
            className="underline font-medium cursor-pointer"
          >
            Cancelar
          </button>
        </div>
      </form>
    </main>
  );
}
