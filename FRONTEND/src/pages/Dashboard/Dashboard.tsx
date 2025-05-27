import { useEffect, useState } from "react";
import axios from "axios";
import type { Cuenta } from "../../types";
import FloatingMenu from "./FloatingMenu";

export default function Dashboard() {
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [cols, setCols] = useState(1);

  async function getCuentas() {
    const response = await axios.get<Cuenta[]>(
      "http://localhost:8001/api/cuentas",
      {
        withCredentials: true,
      }
    );

    if (response.status === 200) {
      setCuentas(response.data);
    }
  }

  useEffect(() => {
    getCuentas();

    const handleResize = () => {
      const w = window.innerWidth;
      if (w >= 1024) setCols(3);
      else if (w >= 768) setCols(2);
      else setCols(1);
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const cuentasVisibles = cuentas.slice(0, 6);

  const necesitaSlotExtra =
    cuentasVisibles.length % cols !== 0 && cuentasVisibles.length < 6;

  return (
    <div className="max-w-5xl mx-auto">
      <div className="p-4 mx-auto">
        <div className="flex justify-center">
          <div className="mt-5 grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 gap-x-10">
            {cuentasVisibles.map((cuenta) => (
              <div
                key={cuenta.id}
                className="w-full h-full p-4 rounded-lg bg-gray-50 dark:bg-orange-400 text-white dark:test-gray-500 flex flex-col justify-between"
              >
                <div>
                  <p className="text-lg font-semibold">
                    Nombre cuenta {cuenta.nombre_cuenta}
                  </p>
                  <p>Saldo cuenta ${cuenta.saldo}</p>
                  <p>Tipo cuenta {cuenta.tipo_cuenta.tipo}</p>
                  <p>
                    Banco: {cuenta.banco.nombre_banco}{" "}
                    <a
                      href={cuenta.banco.url}
                      target="_blank"
                      className="underline text-sm text-blue-200"
                    >
                      Link
                    </a>
                  </p>
                </div>
              </div>
            ))}

            {necesitaSlotExtra && (
              <div className="w-full h-full p-4 rounded-lg bg-white border-2 border-dashed border-gray-300 flex items-center justify-center cursor-pointer hover:bg-gray-100 transition">
                <span className="text-4xl text-gray-400">+</span>
              </div>
            )}
          </div>
        </div>
        <FloatingMenu />
      </div>
    </div>
  );
}
