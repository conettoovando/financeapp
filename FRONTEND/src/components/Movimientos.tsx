import { type Movimientos } from "../types";
import { ChevronLeft, ChevronRight } from "lucide-react";
import clsx from "clsx";

type MovimientosComponentProps = {
  movimientos: Movimientos;
  onPaginate: (url: string) => void;
  modo: string;
};

export default function MovimientosComponent({
  movimientos,
  onPaginate,
  modo = "dashboard", // "dashboard" o "detalle"
}: MovimientosComponentProps) {
  const contenedorClases = clsx(
    "overflow-y-scroll mb-1 outline outline-gray-300 drop-shadow-md",
    {
      "h-[200px]": modo === "dashboard",
      "h-full": modo === "detalle", // toma todo el espacio vertical disponible
    }
  );

  return (
    <>
      <div className="flex justify-between items-end m-0 ">
        <h2 className="text-gray-600 m-0">Últimos movimientos</h2>
        <div className="flex ">
          <button
            className="hover:bg-gray-100 cursor-pointer"
            onClick={() =>
              movimientos.previous && onPaginate(movimientos.previous)
            }
          >
            <ChevronLeft size={18} />
          </button>
          <button
            className="hover:bg-gray-100 cursor-pointer"
            onClick={() => movimientos.next && onPaginate(movimientos.next)}
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
      <section className={contenedorClases}>
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
              movimientos?.results.length > 0 &&
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
    </>
  );
}
