import { useEffect, useState } from "react";
import axios from "axios";
import type { Cuenta, Movimientos, GastosCategoria } from "../../types";
import FloatingMenu from "./FloatingMenu";
import { v4 as uuidv4 } from "uuid";
import { Link } from "react-router";
import { ChevronLeft, ChevronRight, Plus } from "lucide-react"; // ícono opcional

export default function Dashboard() {
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [movimientos, setMovimientos] = useState<Movimientos>();
  const [gastosCategoria, setGastosCategoria] = useState<GastosCategoria[]>([]);

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

  async function getMovimientos(url = "http://localhost:8001/api/movimientos") {
    const response = await axios.get<Movimientos>(url, {
      withCredentials: true,
    });

    if (response.status === 200) {
      setMovimientos(response.data);
    }
  }

  async function getGastosPorCategoria() {
    const response = await axios.get<GastosCategoria[]>(
      "http://localhost:8001/api/estadisticas/gastos-por-categoria",
      { withCredentials: true }
    );

    if (response.status === 200) {
      console.log(response.data);
      setGastosCategoria(response.data);
    }
  }

  useEffect(() => {
    getCuentas();
    getMovimientos();
    getGastosPorCategoria();
  }, []);

  function addCuenta() {
    const nuevaCuenta: Cuenta = {
      nombre_cuenta: "cuenta por boton",
      id: uuidv4(),
      saldo: 0,
      tipo_cuenta: {
        tipo: "",
      },
      banco: {
        nombre_banco: "",
        url: "",
      },
    };

    setCuentas([...cuentas, nuevaCuenta]);
  }

  return (
    <div className="p-4 mx-auto h-[98vh]">
      <div className="flex h-full">
        {/* Contenido central */}
        <main className="flex-1 p-6 space-y-6">
          <button className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-600 hover:shadow-md shadow-sm shadow-gray-400">
            Registrar transacción
          </button>

          {/* Tabla de movimientos */}
          <div className="flex justify-between m-0  align-bottom">
            <h2 className="text-gray-600 mb-1 ">Últimos movimientos</h2>
            <div className="p-0 m-0 flex gap-1">
              <button
                className="hover:bg-gray-100 cursor-pointer"
                onClick={() => {
                  if (movimientos?.previous !== null)
                    return getMovimientos(movimientos?.previous);
                }}
              >
                <ChevronLeft size={18} />
              </button>
              <button
                className="hover:bg-gray-100 cursor-pointer"
                onClick={() => {
                  if (movimientos?.next !== null)
                    return getMovimientos(movimientos?.next);
                }}
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>

          <section className="h-[200px] overflow-y-scroll mb-4 outline outline-gray-300 drop-shadow-md">
            <table className="w-full text-center border-collapse">
              <thead className="sticky top-0 bg-white">
                <tr className="border-b text-gray-600">
                  <th className="py-2">Tipo</th>
                  <th className="py-2">Monto</th>
                  <th className="py-2">Fecha</th>
                  <th className="py-2">Categoría</th>
                </tr>
              </thead>
              <tbody className="min-h-[160px]">
                {movimientos?.results.map((movimiento) => (
                  <tr
                    key={movimiento.id}
                    className="border-b border-gray-300 hover:bg-gray-100"
                  >
                    <td className="py-1">{movimiento.tipo}</td>
                    <td className="py-1">{movimiento.monto}</td>
                    <td className="py-1">
                      {new Date(movimiento.fecha).toLocaleDateString()}
                    </td>
                    <td className="py-1">{movimiento.categoria}</td>
                  </tr>
                ))}

                {/* 👇 Filler rows para mantener el alto visual */}
                {movimientos &&
                  movimientos?.results.length < 4 &&
                  Array.from({ length: 4 - movimientos.results.length }).map(
                    (_, idx) => (
                      <tr
                        key={`filler-${idx}`}
                        className="border-b border-transparent"
                      >
                        <td className="py-1">&nbsp;</td>
                        <td className="py-1">&nbsp;</td>
                        <td className="py-1">&nbsp;</td>
                        <td className="py-1">&nbsp;</td>
                      </tr>
                    )
                  )}
              </tbody>
            </table>
          </section>

          {/* Gastos por categoría */}
          <section className="h-[calc(100%-300px)]">
            <h2 className="text-gray-600 mb-2">Gastos por categoría</h2>
            <div className="grid grid-cols-[0.7fr_1.2fr] gap-4 h-[calc(100%-32px)]">
              {/* Cuadro grande a la izquierda */}
              <div className="bg-gray-100 rounded shadow overflow-y-scroll outline outline-gray-300 p-4 drop-shadow-md">
                <table className="w-full text-left">
                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Monto</th>
                    </tr>
                  </thead>
                  <tbody>
                    {gastosCategoria.map((elemento) => (
                      <tr>
                        <td>{elemento.categoria}</td>
                        <td>{elemento.total}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Columna con gráfico y calendario */}
              <div className="flex flex-col gap-4 ">
                <div className="bg-white flex-1 flex items-center justify-center rounded outline outline-gray-300 p-4 drop-shadow-md">
                  GRAFICO DE GASTOS
                </div>
                <div className="bg-white flex-1 flex items-center justify-center rounded outline outline-gray-300 p-4 drop-shadow-md">
                  CALENDARIO
                </div>
              </div>
            </div>
          </section>
        </main>

        {/* Sidebar derecha */}
        <aside className="w-80 p-4 bg-white space-y-4 h-full overflow-y-auto">
          {cuentas.map((cuenta) => (
            <Link
              to={`/cuenta/${cuenta.id}`}
              className="block bg-gray-300 p-4 rounded hover:bg-gray-200 h-35 outline outline-gray-300 drop-shadow-md"
              key={cuenta.id}
            >
              <h1 className="font-semibold text-lg">{cuenta.nombre_cuenta}</h1>
              <p className="text-md">
                {Intl.NumberFormat("cl-CL", {
                  style: "currency",
                  currency: "CLP",
                }).format(cuenta.saldo)}
              </p>
              <div className="pt-4 text-sm">
                <a
                  href={cuenta.banco.url}
                  target="_blank"
                  className="italic leading-0"
                >
                  {cuenta.banco.nombre_banco}
                </a>
                <p className="italic leading-2">{cuenta.tipo_cuenta.tipo}</p>
              </div>
            </Link>
          ))}

          <div
            className="bg-gray-300 h-35 flex items-center justify-center rounded cursor-pointer hover:bg-gray-200 transition"
            onClick={() => addCuenta()}
          >
            <span className="text-4xl text-gray-400">+</span>
          </div>
        </aside>
      </div>
    </div>
  );
}
