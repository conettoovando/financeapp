export interface Cuenta {
  id: string;
  nombre_cuenta: string;
  saldo: number;
  tipo_cuenta: {
    tipo: string;
  };
  banco: {
    nombre_banco: string;
    url: string;
  };
}