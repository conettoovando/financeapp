import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import Container from "../../components/Container";
import MovimientosComponent from "../../components/Movimientos";
import type { Movimientos } from "../../types";
import { getMovimientos } from "../../services/movimientosService";

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

  useEffect(() => {
    async function obtenerCuenta() {
      const response = await axios.get<cuenta>(
        `http://localhost:8001/api/cuentas/${params.cuenta_id}`,
        { withCredentials: true }
      );
      setCuenta(response.data);
    }

    async function obtenerMovimientos() {
      const data = await getMovimientos(
        `http://localhost:8001/api/movimientos?cuenta_id=${params.cuenta_id}&limit10&offset=0&orden=desc`
      );
      console.log(data);
      setMovimientos(data);
    }

    obtenerCuenta();
    obtenerMovimientos();
  }, [params.cuenta_id]);

  return (
    <Container>
      <div className="flex flex-col w-full h-full items-center">
        <div className="m-2 bg-orange-300 w-[35rem] outline outline-gray-500">
          <div className="p-2 mb-5">
            <div className="block w-full border border-gray-500 border-dashed border-l-0 border-t-0 border-r-0">
              <h1 className="text-xl ">{cuenta?.nombre_cuenta}</h1>
            </div>
            <p className="flex w-full justify-between pt-2">
              {cuenta?.banco.nombre_banco}{" "}
              <a
                href={cuenta?.banco.url}
                target="_blank"
                className="text-blue-600 underline hover:text-blue-400"
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
                  <div className="text-end">
                    <p>Fecha de facturación</p>
                    <p>
                      {new Date(cuenta.fecha_facturacion).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="text-end">
                    <p>Fecha de pago</p>
                    <p>{new Date(cuenta.fecha_pago).toLocaleDateString()}</p>
                  </div>
                </>
              )}
            </section>
          </div>
        </div>
        <div className="w-full h-[calc(100vh-275px)]">
          <MovimientosComponent
            movimientos={movimientos!}
            onPaginate={(url) => getMovimientos(url).then(setMovimientos)}
            modo="detalle"
          />
        </div>
      </div>
    </Container>
  );
}
