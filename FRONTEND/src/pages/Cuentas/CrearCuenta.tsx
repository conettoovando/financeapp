import axios from "axios";
import { useEffect, useState } from "react";
import { Controller, useForm, useWatch } from "react-hook-form";
import { useNavigate } from "react-router";
import Select from "react-select";
import financeApi from "../../api/financeApi";

type Nuevacuenta = {
  nombre_cuenta: string;
  tipo_cuenta_id: string;
  banco_id: string;
  saldo: number;
  limite_credito: number | null;
  fecha_facturacion: string | null;
  fecha_pago: string | null;
};

type NuevacuentaResponse = {
  message: string;
  data: {
    id: string;
    nombre_cuenta: string;
    tipo_cuenta_id: string;
    banco_id: string;
    saldo: number;
    limite_credito: number | null;
    fecha_facturacion: string | null;
    fecha_pago: string | null;
  };
};

type TipoCuenta = {
  id: string;
  tipo: string;
};

type Banco = {
  id: string;
  nombre_banco: string;
  url: string;
};

type FormData = {
  tipo_cuenta: TipoCuenta[];
  banco: Banco[];
};

export default function CrearCuenta() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    control,
  } = useForm<Nuevacuenta>();
  const [tipoCuentas, setTipocuentas] = useState<TipoCuenta[]>();
  const [bancos, setBancos] = useState<Banco[]>();
  // const [tipoCuentaSeleccionada, setTipoCuentaSeleccionada] =
  //   useState<TipoCuenta | null>(null);
  const tipoCuentaId = useWatch({ control, name: "tipo_cuenta_id" });
  const tipoCuentaSeleccionada = tipoCuentas?.find(
    (tc) => tc.id === tipoCuentaId
  );
  const navigator = useNavigate();

  const onSubmit = handleSubmit(async (data) => {
    try {
      const response = await financeApi.post<NuevacuentaResponse>(
        "/cuentas",
        data
      );

      if (response.status === 200) {
        navigator(`/tabs/cuenta/${response.data.data.id}`);
      }
    } finally {
      reset();
    }
  });

  useEffect(() => {
    async function obtenerDatos() {
      const response = await financeApi.get<FormData>("forms/createCuenta");

      if (response.status === 200) {
        setTipocuentas(response.data.tipo_cuenta);
        setBancos(response.data.banco);
      }
    }

    obtenerDatos();
  }, []);

  return (
    <main className="container h-screen grid place-items-center mx-auto overflow-y-auto">
      <form
        className="flex flex-col gap-5 items-center border border-slate-700 rounded-md w-full max-w-md px-8 py-10"
        onSubmit={onSubmit}
      >
        <div className="space-y-4">
          <h1 className="text-2xl font-bold text-center">Crear nueva cuenta</h1>
        </div>

        <div className="space-y-3 w-full">
          <div className="flex flex-col gap-2">
            <label
              htmlFor="nombre_cuenta"
              className="text-sm text-slate-700 font-semibold"
            >
              Nombre de la cuenta
            </label>

            <input
              type="nombre_cuenta"
              id="nombre_cuenta"
              className={`border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600`}
              placeholder="Mi cuenta"
              {...register("nombre_cuenta", {
                required: "Se requiere asignarle un nombre a la cuenta",
              })}
            />
            {errors.nombre_cuenta && (
              <p className="text-red-500 font-medium text-sn w-full">
                {errors.nombre_cuenta.message}
              </p>
            )}
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm text-slate-700 font-semibold"
            >
              Tipo de Cuenta{" "}
            </label>

            <Controller
              name="tipo_cuenta_id"
              control={control}
              rules={{ required: true }}
              render={({ field }) => (
                <Select
                  {...field}
                  options={tipoCuentas}
                  getOptionLabel={(option) => option.tipo}
                  getOptionValue={(option) => option.id}
                  value={tipoCuentas?.find((c) => c.id === field.value) || null}
                  onChange={(option) => {
                    const tipoCuenta = option as TipoCuenta;
                    field.onChange(tipoCuenta?.id || "");
                    // setTipoCuentaSeleccionada(tipoCuenta);
                  }}
                  isClearable
                  placeholder="Seleccione un tipo de cuenta"
                />
              )}
            />
            {errors.tipo_cuenta_id && (
              <p className="text-red-500 font-medium text-sn w-full">
                {errors.tipo_cuenta_id.message}
              </p>
            )}
          </div>

          <div className="flex flex-col gap-2">
            <label
              htmlFor="email"
              className="text-sm text-slate-700 font-semibold"
            >
              Tipo de Cuenta{" "}
            </label>

            <Controller
              name="banco_id"
              control={control}
              rules={{ required: true }}
              render={({ field }) => (
                <Select
                  {...field}
                  options={bancos}
                  getOptionLabel={(option) => option.nombre_banco}
                  getOptionValue={(option) => option.id}
                  value={bancos?.find((c) => c.id === field.value) || null}
                  onChange={(option) =>
                    field.onChange(option ? (option as Banco).id : "")
                  }
                  isClearable
                  placeholder="Seleccione un tipo de cuenta"
                />
              )}
            />
            {errors.tipo_cuenta_id && (
              <p className="text-red-500 font-medium text-sn w-full">
                {errors.banco_id?.message}
              </p>
            )}
          </div>

          {tipoCuentaSeleccionada?.tipo === "Tarjeta de Crédito" ? (
            <>
              {/* Límite de crédito (ya agregado antes) */}
              <div className="flex flex-col gap-2">
                <label
                  htmlFor="limite_credito"
                  className="text-sm text-slate-700 font-semibold"
                >
                  Límite de Crédito
                </label>
                <input
                  type="number"
                  id="limite_credito"
                  className="border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600"
                  defaultValue={0}
                  {...register("limite_credito", {
                    required: "Ingrese el límite de crédito",
                    min: 100000, // puedes ajustar esto
                  })}
                />
                {errors.limite_credito && (
                  <p className="text-red-500 font-medium text-sn w-full">
                    {errors.limite_credito.message}
                  </p>
                )}
              </div>

              <div className="flex flex-col gap-2">
                <label
                  htmlFor="fecha_facturacion"
                  className="text-sm text-slate-700 font-semibold"
                >
                  Fecha de Facturación
                </label>
                <input
                  type="datetime-local"
                  id="fecha_facturacion"
                  className="border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600"
                  {...register("fecha_facturacion", {
                    required: "Ingrese la fecha de facturación",
                  })}
                />
                {errors.fecha_facturacion && (
                  <p className="text-red-500 font-medium text-sn w-full">
                    {errors.fecha_facturacion.message}
                  </p>
                )}
              </div>

              <div className="flex flex-col gap-2">
                <label
                  htmlFor="fecha_pago"
                  className="text-sm text-slate-700 font-semibold"
                >
                  Fecha de Pago
                </label>
                <input
                  type="datetime-local"
                  id="fecha_pago"
                  className="border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600"
                  {...register("fecha_pago", {
                    required: "Ingrese la fecha de pago",
                  })}
                />
                {errors.fecha_pago && (
                  <p className="text-red-500 font-medium text-sn w-full">
                    {errors.fecha_pago.message}
                  </p>
                )}
              </div>
            </>
          ) : (
            <div className="flex flex-col gap-2">
              <label
                htmlFor="nombre_cuenta"
                className="text-sm text-slate-700 font-semibold"
              >
                Saldo de la cuenta
              </label>

              <input
                type="number"
                min={0}
                step="1"
                pattern="[0-9]*"
                id="saldo"
                className={`border rounded-sm px-2 py-3 text-sm outline-none font-medium text-slate-600`}
                defaultValue={0}
                {...register("saldo", {
                  required: "Se requiere asignarle un saldo",
                })}
              />
              {errors.saldo && (
                <p className="text-red-500 font-medium text-sn w-full">
                  {errors.saldo.message}
                </p>
              )}
            </div>
          )}
        </div>

        <div className="flex flex-col gap-3 w-full">
          <button
            type="submit"
            className="bg-stone-800 text-white py-3 rounded-md font-medium cursor-pointer"
          >
            Ingresar
          </button>
          <button
            onClick={() => {
              window.history.back();
            }}
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
