import Container from "../../components/Container";
import { Controller, useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import Select from "react-select";
import { useNavigate, useSearchParams } from "react-router"; // Importa useSearchParams
import financeApi from "../../api/financeApi";

type CrearMovimiento = {
  cuenta_id: string;
  movimiento_id: string;
  monto: number;
  fecha: string;
  categoria_id: string;
  destinatario_id: null | string;
};

type CategoriasResponse = {
  id: string;
  nombre: string;
  usuario_id: string | null;
};

type Cuenta = {
  id: string;
  nombre_cuenta: string;
};

type TipoMovimientos = {
  id: string;
  tipo: string;
};

type CrearMovimientoFormResponse = {
  cuentas: Cuenta[];
  tipo_movimientos: TipoMovimientos[];
  categorias: CategoriasResponse[];
};

const soloNumeros = (event: React.KeyboardEvent<HTMLInputElement>) => {
  const tecla = event.key;
  if (
    (tecla >= "0" && tecla <= "9") ||
    ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Tab"].includes(tecla)
  )
    return;
  event.preventDefault();
};

const limpiarPegado = (event: React.FormEvent<HTMLInputElement>) => {
  const input = event.currentTarget;
  input.value = input.value.replace(/\D/g, "");
};

const obtenerFechaParaInput = () => {
  const now = new Date();
  const offset = now.getTimezoneOffset();
  const localDate = new Date(now.getTime() - offset * 60000);
  return localDate.toISOString().slice(0, 16);
};

export default function CrearMovimiento() {
  const navigator = useNavigate();
  const [searchParams] = useSearchParams(); // Hook para leer los query params
  const cuentaIdFromQuery = searchParams.get("cuenta_id"); // Obtener 'cuenta_id' del query param

  const {
    register,
    reset,
    handleSubmit,
    formState: { errors },
    control,
    setValue, // Necesitamos setValue para actualizar el campo de la cuenta programáticamente
  } = useForm<CrearMovimiento>({
    defaultValues: {
      fecha: obtenerFechaParaInput(),
      // Por ahora, cuenta_id es null, lo estableceremos en el useEffect
      cuenta_id: "",
    },
  });

  const [cuentas, setCuentas] = useState<Cuenta[]>([]); // Renombrado a 'cuentas' para mayor claridad
  const [tipoMovimiento, setTipoMovimientos] = useState<TipoMovimientos[]>([]);
  const [categoria, setCategorias] = useState<CategoriasResponse[]>([]);

  const onSubmit = handleSubmit(async (data) => {
    const response = await financeApi.post("/movimientos/", data);

    if (response.status === 200) {
      reset();
    }

    navigator(`/tabs/cuenta/${data.cuenta_id}`);
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await financeApi.get<CrearMovimientoFormResponse>(
          "/forms/crearMovimiento"
        );
        if (response.status === 200) {
          const {
            cuentas: fetchedCuentas, // Renombrado para evitar conflicto con el estado 'cuentas'
            tipo_movimientos: fetchedTipoMovimientos,
            categorias: fetchedCategorias,
          } = response.data;
          setCuentas(fetchedCuentas);
          setTipoMovimientos(fetchedTipoMovimientos);
          setCategorias(fetchedCategorias);

          // Si hay un cuenta_id en los query params, lo establecemos
          if (cuentaIdFromQuery) {
            const cuentaASeleccionar = fetchedCuentas.find(
              (c) => c.id === cuentaIdFromQuery
            );
            if (cuentaASeleccionar) {
              setValue("cuenta_id", cuentaASeleccionar.id);
            } else {
              console.warn(`Cuenta con ID ${cuentaIdFromQuery} no encontrada.`);
            }
          }
        }
      } catch (error) {
        console.error("Error al cargar datos del formulario:", error);
        // Manejo de errores, por ejemplo, mostrar un mensaje al usuario
      }
    };

    const initialDate = obtenerFechaParaInput();
    reset({
      fecha: initialDate,
      // No reseteamos cuenta_id aquí para que el valor del query param tenga prioridad
      // Se establecerá después de cargar las cuentas si cuentaIdFromQuery existe
    });

    fetchData();
    // Añadir dependencias necesarias para useEffect
  }, [reset, cuentaIdFromQuery, setValue]); // `setValue` es una dependencia estable proporcionada por `useForm`

  return (
    <Container>
      <div className="flex bg-red-600 justify-center h-full">
        <form onSubmit={onSubmit} className="w-80 bg-yellow-400">
          <label>Cuenta</label>
          <Controller
            name="cuenta_id"
            control={control}
            rules={{ required: "La cuenta es obligatoria" }}
            render={({ field }) => (
              <Select
                {...field}
                options={cuentas} // Usar el estado 'cuentas'
                getOptionLabel={(option) => option.nombre_cuenta}
                getOptionValue={(option) => option.id}
                value={cuentas?.find((c) => c.id === field.value) || null}
                onChange={(option) => {
                  const selectedCuenta = option as Cuenta;
                  field.onChange(selectedCuenta?.id || "");
                }}
                isClearable
                placeholder="Seleccione una cuenta"
              />
            )}
          />
          {errors.cuenta_id && (
            <span className="text-red-500 text-sm flex">
              {errors.cuenta_id.message}
            </span>
          )}

          <label>Tipo de movimiento</label>
          <Controller
            name="movimiento_id"
            control={control}
            rules={{ required: "El tipo de movimiento es obligatorio" }}
            render={({ field }) => (
              <Select
                {...field}
                options={tipoMovimiento}
                getOptionLabel={(option) => option.tipo}
                getOptionValue={(option) => option.id}
                value={
                  tipoMovimiento?.find((c) => c.id === field.value) || null
                }
                onChange={(option) => {
                  const movimiento = option as TipoMovimientos;
                  field.onChange(movimiento?.id || "");
                }}
                isClearable
                placeholder="Seleccione un tipo de movimiento"
              />
            )}
          />
          {errors.movimiento_id && (
            <span className="text-red-500 text-sm flex">
              {errors.movimiento_id.message}
            </span>
          )}

          <label>Monto</label>
          <input
            {...register("monto", {
              required: "El monto es obligatorio",
              valueAsNumber: true,
              validate: (value) =>
                (Number.isInteger(value) && value >= 0) ||
                "Solo números enteros positivos",
            })}
            className="flex w-full bg-white h-[36px] py-[2px] px-[8px] rounded-sm"
            type="text"
            onKeyDown={(e) => {
              soloNumeros(e);
              if (e.key === "Enter") {
                e.preventDefault();
                onSubmit();
              }
            }}
            onInput={limpiarPegado}
          />
          {errors.monto && (
            <span className="text-red-500 text-sm flex">
              {errors.monto.message}
            </span>
          )}

          <label htmlFor="fecha">Fecha y hora del movimiento</label>
          <input
            type="datetime-local"
            id="fecha"
            className="border rounded-sm px-2 py-3 text-sm outline-none font-medium bg-white w-full"
            {...register("fecha", {
              required: "Ingrese la fecha del movimiento",
            })}
          />
          {errors.fecha && (
            <p className="text-red-500">{errors.fecha.message}</p>
          )}

          <label>Categoría</label>
          <Controller
            name="categoria_id"
            control={control}
            rules={{ required: "La categoría es obligatoria" }}
            render={({ field }) => (
              <Select
                {...field}
                options={categoria}
                getOptionLabel={(option) => option.nombre}
                getOptionValue={(option) => option.id}
                value={categoria?.find((c) => c.id === field.value) || null}
                onChange={(option) => {
                  const selectedCategoria = option as CategoriasResponse;
                  field.onChange(selectedCategoria?.id || "");
                }}
                isClearable
                placeholder="Seleccione una categoría"
              />
            )}
          />
          {errors.categoria_id && (
            <span className="text-red-500 text-sm flex">
              {errors.categoria_id.message}
            </span>
          )}

          <div className="flex justify-center">
            <button
              type="submit"
              className="bg-red-400 w-40 cursor-pointer rounded-2xl py-1"
            >
              Enviar
            </button>
          </div>
        </form>
      </div>
    </Container>
  );
}
