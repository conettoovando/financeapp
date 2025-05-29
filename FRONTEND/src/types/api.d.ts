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

export interface Movimientos {
  count: number;
  next: string;
  previous: string;
  results: Movimiento[];
}

export interface Movimiento {
  id: string;
  tipo: string;
  monto: number;
  fecha: Date;
  categoria: string;
  destinatario: {
    nombre: string
  }
}

export interface GastosCategoria {
  categoria: string;
  total: number
}