import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router";
import Container from "../../components/Container";
import MovimientosComponent from "../../components/Movimientos";
import type { Movimientos } from "../../types";
import { getMovimientos } from "../../services/movimientosService";
import { CirclePlus, SquarePen, Trash2 } from "lucide-react";
import financeApi from "../../api/financeApi";
import { useAuth } from "../../context/useAuth";

type params = {
  cuenta_id: string;
};

type cuenta = {
  id: string;
  nombre_cuenta: string | null;
  saldo: number;
  limite_credito: number | null;
  fecha_facturacion: string;
  fecha_pago: string;
  tipo_cuenta: {
    tipo: string;
  };
  banco: {
    nombre_banco: string;
    url: string;
  };
};

export default function VerCuenta() {
  const params = useParams<params>();
  const [cuenta, setCuenta] = useState<cuenta>();
  const [movimientos, setMovimientos] = useState<Movimientos>();
  const navigator = useNavigate();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (isLoading || !isAuthenticated) return;

    async function obtenerCuenta() {
      try {
        const response = await financeApi.get<cuenta>(
          `/cuentas/${params.cuenta_id}`
        );
        setCuenta(response.data);
      } catch (error) {
        console.error("Error al obtener cuenta", error);
      }
    }

    async function obtenerMovimientos() {
      try {
        const data = await getMovimientos(
          `/movimientos?cuenta_id=${params.cuenta_id}&limit=10&offset=0&orden=desc`
        );
        setMovimientos(data);
      } catch (error) {
        console.error("Error al obtener movimientos", error);
      }
    }

    obtenerCuenta();
    obtenerMovimientos();
  }, [params.cuenta_id, isAuthenticated, isLoading]);

  return (
    <Container>
      <div className="flex flex-col w-full h-full items-center">
        <div className="bg-linear-to-b/oklab from-gray-700 via-gray-500 to-gray-400  w-[35rem] outline outline-gray-500 rounded-xl">
          <div className="p-2 mb-5">
            <div className="block w-full border border-gray-500 border-dashed border-l-0 border-t-0 border-r-0">
              <h1 className="text-xl text-white">{cuenta?.nombre_cuenta}</h1>
            </div>
            <p className="flex w-full justify-between pt-2">
              {cuenta?.banco.nombre_banco}{" "}
              <a
                href={cuenta?.banco.url}
                target="_blank"
                className="text-blue-500 underline hover:text-blue-200"
              >
                Sitio Web
              </a>
            </p>

            <p>{cuenta?.tipo_cuenta.tipo}</p>
            <section className="flex mt-5 justify-between">
              <div>
                <p className="text-gray-700">Saldo disponible</p>
                <p className="text-md">
                  {Intl.NumberFormat("cl-CL", {
                    style: "currency",
                    currency: "CLP",
                  }).format(cuenta?.saldo ?? 0)}
                </p>
              </div>
              {cuenta?.tipo_cuenta.tipo.toLowerCase() ===
                "tarjeta de crédito" && (
                <>
                  <div className="text-center">
                    <p>Fecha de facturación</p>
                    <p>
                      {new Date(cuenta.fecha_facturacion).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-center">
                    <p>Fecha de pago</p>
                    <p>{new Date(cuenta.fecha_pago).toLocaleDateString()}</p>
                  </div>
                </>
              )}
            </section>
          </div>
        </div>
        <div className="flex align-middle w-[25%] px-10 mt-5  justify-between">
          <button
            onClick={() => {
              navigator(
                `/tabs/actions/crear-movimiento?cuenta_id=${params.cuenta_id}`
              );
            }}
            className="bg-orange-400 rounded-full p-2 cursor-pointer text-white hover:bg-orange-300 hover:text-gray-200"
          >
            <CirclePlus size={25} />
          </button>
          <button className="bg-orange-400 rounded-full p-2 cursor-pointer text-white hover:bg-orange-300 hover:text-gray-200">
            <SquarePen size={25} />
          </button>
          <button className="bg-orange-400 rounded-full p-2 cursor-pointer text-white hover:bg-orange-300 hover:text-gray-200">
            <Trash2 size={25} />
          </button>
        </div>
        <div className="w-full h-[calc(100vh-275px)]">
          <MovimientosComponent
            movimientos={movimientos!}
            onPaginate={(url) => getMovimientos(url).then(setMovimientos)}
            modo="dashboard"
          />
        </div>
      </div>
    </Container>
  );
}
