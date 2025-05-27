import { useState } from "react";
import { Plus } from "lucide-react"; // ícono opcional

export default function FloatingMenu() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Versión normal para pantallas medianas hacia arriba */}
      <div className="hidden md:flex p-5 max-w-3xl mx-auto justify-between gap-5 h-fit">
        <button
          onClick={() => alert("Nuevo movimiento")}
          className="p-2.5 border rounded-2xl border-gray-500 w-full"
        >
          Nuevo movimiento
        </button>
        <button className="p-2.5 border rounded-2xl border-gray-500 w-full">
          Ingreso
        </button>
        <button className="p-2.5 border rounded-2xl border-gray-500 w-full">
          Gasto
        </button>
        <button className="p-2.5 border rounded-2xl border-gray-500 w-full">
          Transferencia
        </button>
      </div>

      {/* Floating Button + Menu (solo visible en pantallas pequeñas) */}
      <div className="md:hidden fixed bottom-5 right-5 z-50 flex flex-col items-end gap-2">
        {/* Opciones desplegadas */}
        {open && (
          <div className="flex flex-col gap-2 mb-2 animate-fade-in">
            <button
              className="bg-white border rounded-lg px-4 py-2 shadow"
              onClick={() => alert("Nuevo movimiento")}
            >
              Nuevo movimiento
            </button>
            <button className="bg-white border rounded-lg px-4 py-2 shadow">
              Ingreso
            </button>
            <button className="bg-white border rounded-lg px-4 py-2 shadow">
              Gasto
            </button>
            <button className="bg-white border rounded-lg px-4 py-2 shadow">
              Transferencia
            </button>
          </div>
        )}

        {/* Botón flotante */}
        <button
          onClick={() => setOpen(!open)}
          className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition"
        >
          <Plus className={`transition-transform ${open ? "rotate-45" : ""}`} />
        </button>
      </div>
    </>
  );
}
