CREATE DATABASE IF NOT EXISTS finance;
USE finance;

CREATE TABLE IF NOT EXISTS Users(
	id BINARY(16) primary key not null default (UUID_TO_BIN(UUID())),
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp ON update current_timestamp
);

create table if not exists Destinatario(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
	usuario_id binary(16) not null,
    nombre varchar(50) not null,
    FOREIGN KEY (usuario_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Banco(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
    nombre_banco varchar(30) not null,
    url varchar(90)
);

CREATE TABLE IF NOT EXISTS TipoCuenta(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
	tipo varchar(30) not null
);

CREATE TABLE IF NOT EXISTS Cuenta(
	id BINARY(16) primary key not null default (UUID_TO_BIN(UUID())),
    nombre_cuenta VARCHAR(30),
    tipo_cuenta_id BINARY(16) NOT NULL,
    saldo INT DEFAULT 0,
    banco_id BINARY(16) NOT NULL,
    limite_credito int default null,
    fecha_facturacion datetime default null,
    fecha_pago datetime default null,
    user_id BINARY(16) NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp,
    updated_at DATETIME DEFAULT current_timestamp ON update current_timestamp,
    foreign key (tipo_cuenta_id) references TipoCuenta(id) on delete restrict,
    foreign key (banco_id) references Banco(id) on delete cascade,
    foreign key (user_id) references Users(id) on delete cascade
);

create table if not exists TipoMovimiento(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
	tipo varchar(30) not null
);

create table if not exists Categoria(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
	nombre varchar(30) not null
);

CREATE TABLE IF NOT EXISTS Movimiento(
	id binary(16) primary key not null default (UUID_TO_BIN(UUID())),
	cuenta_id binary(16) not null,
    usuario_id binary(16) not null,
    tipoMovimiento_id binary(16) not null,
    monto int not null default 0,
    fecha datetime default current_timestamp,
    categoria_id binary(16) not null,
    destinatario_id binary(16),
    foreign key (cuenta_id) references Cuenta(id) on delete cascade,
    foreign key (usuario_id) references Users(id) on delete cascade,
    foreign key (tipoMovimiento_id) references TipoMovimiento(id) on delete restrict,
    foreign key (categoria_id) references Categoria(id) on delete restrict,
    foreign key (destinatario_id) references Destinatario(id) on delete set null
);

