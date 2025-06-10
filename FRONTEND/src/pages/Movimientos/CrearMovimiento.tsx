import Container from "../../components/Container";
import { Controller, useForm } from "react-hook-form";
import axios from "axios";
import { useEffect } from "react";
import { useState } from "react";
import { type Cuenta } from "../../types";
import Select from "react-select";

type CrearMovimiento = {
  cuenta_id: string;
  movimiento_id: string;
  monto: number;
  fecha: string;
  categoria_id: string;
  destinatario_id: null | string;
};

type CrearCuenta = {
  tipo_cuenta: {
    id: string;
    tipo: string;
  };
  banco: {
    id: string;
    nombre_banco: string;
    url: string;
  };
};

export default function CrearMovimiento() {
  const {
    register,
    reset,
    handleSubmit,
    formState: { errors },
    control,
  } = useForm<CrearMovimiento>();
  const [cuentas, setCuentas] = useState<Cuenta[]>([]);

  const onSubmit = handleSubmit(async (data) => {
    return data;
  });

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get<Cuenta[]>(
        "http://localhost:8001/api/cuentas",
        {
          withCredentials: true,
        }
      );
      if (response.status === 200) {
        setCuentas(response.data);
      }
    };

    fetchData();
  }, []);

  return (
    <Container>
      <div className="flex bg-red-600 justify-center h-full">
        <form action="" onSubmit={onSubmit}>
          <Controller
            name="cuenta_id"
            control={control}
            rules={{ required: true }}
            render={({ field }) => (
              <Select
                {...field}
                options={cuentas}
                getOptionLabel={(option) => option.nombre_cuenta}
                getOptionValue={(option) => option.id}
                value={cuentas?.find((c) => c.id === field.value) || null}
                onChange={(option) => {
                  const cuenta = option as Cuenta;
                  field.onChange(cuenta?.id || "");
                  // setTipoCuentaSeleccionada(tipoCuenta);
                }}
                isClearable
                placeholder="Seleccione un tipo de cuenta"
              />
            )}
          />
        </form>
      </div>
    </Container>
  );
}
