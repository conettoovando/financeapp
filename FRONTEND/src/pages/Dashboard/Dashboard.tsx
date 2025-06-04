import { useEffect, useState } from "react";
import axios from "axios";
import type { Cuenta, Movimientos, GastosCategoria } from "../../types";
import { Link, useNavigate } from "react-router";
import Container from "../../components/Container";
import { getMovimientos } from "../../services/movimientosService";
import MovimientosComponent from "../../components/Movimientos";

export default function Dashboard() {
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);
  const [movimientos, setMovimientos] = useState<Movimientos>();
  const [gastosCategoria, setGastosCategoria] = useState<GastosCategoria[]>([]);
  const navigate = useNavigate();

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

  async function getGastosPorCategoria() {
    const response = await axios.get<GastosCategoria[]>(
      "http://localhost:8001/api/estadisticas/gastos-por-categoria",
      { withCredentials: true }
    );

    if (response.status === 200) {
      setGastosCategoria(response.data);
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      const data = await getMovimientos();
      setMovimientos(data);
    };
    getCuentas();
    getGastosPorCategoria();
    fetchData();
  }, []);

  function addCuenta() {
    return navigate("/tabs/cuenta/add-cuenta");
  }

  return (
    <Container>
      <div className="flex h-full">
        {/* Contenido central */}
        <main className="flex-1 p-6 space-y-6">
          <button className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-600 hover:shadow-md shadow-sm shadow-gray-400">
            Registrar transacción
          </button>

          {/* Tabla de movimientos */}
          <MovimientosComponent
            movimientos={movimientos!}
            onPaginate={(url) => getMovimientos(url).then(setMovimientos)}
          />

          {/* Gastos por categoría */}
          <section className="h-[calc(100%-300px)]">
            <h2 className="text-gray-600 mb-2">Gastos por categoría</h2>
            <div className="grid grid-cols-[0.7fr_1.2fr] gap-4 h-[calc(100%-32px)]">
              {/* Cuadro grande a la izquierda */}
              <div className="bg-gray-100 rounded shadow overflow-y-scroll outline outline-gray-300 p-4 drop-shadow-md">
                <table className="w-full text-center border-collapse">
                  <thead className="sticky top-0">
                    <tr className="border-b text-gray-600">
                      <th>Nombre</th>
                      <th>Monto</th>
                    </tr>
                  </thead>
                  <tbody className="border-b border-gray-300 hover:bg-gray-100">
                    {gastosCategoria.map((elemento) => (
                      <tr
                        key={elemento.categoria}
                        className="border-b border-gray-300 hover:bg-gray-100"
                      >
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
              to={`/tabs/cuenta/${cuenta.id}`}
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
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    window.open(cuenta.banco.url, "_blank");
                  }}
                  className="italic leading-0 underline text-blue-500 hover:text-blue-700 cursor-pointer"
                >
                  {cuenta.banco.nombre_banco}
                </button>
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
    </Container>
  );
}
