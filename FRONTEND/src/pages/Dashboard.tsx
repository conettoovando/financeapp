import { useEffect, useState } from "react";
import axios from "axios";
import type { Cuenta } from "../types";

export default function Dashboard() {
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);

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
  }, []);

  return (
    <div className="flex justify-center bg-amber-600">
      <div className="mt-5 grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 gap-x-10 mb-4">
        {cuentas.map((cuenta) => {
          return (
            <div
              key={cuenta.id}
              className="flex-row items-center justify-center p-4 max-w-100 rounded-lg bg-gray-50 dark:bg-gray-800 text-white dark:test-gray-500"
            >
              <p className="text-xl font-semibold">
                Nombre cuenta {cuenta.nombre_cuenta}
              </p>
              <div>
                <p>Saldo cuenta ${cuenta.saldo}</p>
                <p>Tipo cuenta {cuenta.tipo_cuenta.tipo}</p>
                <p>
                  banco cuenta {cuenta.banco.nombre_banco}{" "}
                  <a href={cuenta.banco.url} target="_blank">
                    Link
                  </a>
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
