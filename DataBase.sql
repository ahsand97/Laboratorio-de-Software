BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `usuarios` (
	`id`	INTEGER NOT NULL,
	`Nombre`	TEXT NOT NULL,
	`Usuario`	TEXT NOT NULL,
	`Correo`	TEXT NOT NULL,
	`Clave`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `transferencias` (
	`id`	INTEGER NOT NULL,
	`id_Transaccion`	INTEGER NOT NULL,
	`id_CuentaDestino`	INTEGER NOT NULL,
	FOREIGN KEY(`id_Transaccion`) REFERENCES `transacciones`(`id`),
	FOREIGN KEY(`id_CuentaDestino`) REFERENCES `cuentas`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `transacciones` (
	`id`	INTEGER NOT NULL,
	`Fecha`	TEXT NOT NULL,
	`Valor`	REAL NOT NULL,
	`Descripcion`	TEXT,
	`id_Cuenta`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Cuenta`) REFERENCES `cuentas`(`id`)
);
CREATE TABLE IF NOT EXISTS `transaccion_presupuesto_cuenta` (
	`id_Transaccion`	INTEGER,
	`id_Presupuesto_cuenta`	INTEGER,
	FOREIGN KEY(`id_Presupuesto_cuenta`) REFERENCES `presupuesto_cuenta`(`id`),
	FOREIGN KEY(`id_Transaccion`) REFERENCES `transacciones`(`id`)
);
CREATE TABLE IF NOT EXISTS `tipocuenta` (
	`id`	INTEGER NOT NULL,
	`Nombre`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `reembolsos` (
	`id`	INTEGER NOT NULL,
	`id_Cheque`	INTEGER NOT NULL,
	`id_Transaccion`	INTEGER NOT NULL,
	FOREIGN KEY(`id_Cheque`) REFERENCES `cheques`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Transaccion`) REFERENCES `transacciones`(`id`)
);
CREATE TABLE IF NOT EXISTS `presupuestos` (
	`id`	INTEGER NOT NULL,
	`Saldo`	REAL NOT NULL,
	`Nombre`	TEXT NOT NULL,
	`Estado`	BOOLEAN NOT NULL,
	`id_Categoria`	INTEGER NOT NULL,
	`id_Moneda`	INTEGER NOT NULL,
	CHECK("Estado"IN(0,1)),
	FOREIGN KEY(`id_Categoria`) REFERENCES `categorias`(`id`),
	FOREIGN KEY(`id_Moneda`) REFERENCES `monedas`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `presupuesto_cuenta` (
	`id`	INTEGER NOT NULL,
	`id_Cuenta`	INTEGER NOT NULL,
	`id_Presupuesto`	INTEGER NOT NULL,
	FOREIGN KEY(`id_Cuenta`) REFERENCES `cuentas`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Presupuesto`) REFERENCES `presupuestos`(`id`)
);
CREATE TABLE IF NOT EXISTS `prestamos` (
	`id`	INTEGER NOT NULL,
	`TAE`	INTEGER NOT NULL,
	`Cuotas`	INTEGER NOT NULL,
	`Valor_Prestamo`	REAL NOT NULL,
	`id_Cuenta`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Cuenta`) REFERENCES `cuentas`(`id`)
);
CREATE TABLE IF NOT EXISTS `pago_prestamo` (
	`id`	INTEGER NOT NULL,
	`Dia_Pago`	TEXT NOT NULL,
	`Pago_Completo`	BOOLEAN NOT NULL,
	`Valor_Pagar`	REAL NOT NULL,
	`id_Prestamo`	INTEGER NOT NULL,
	CHECK("Pago_Completo"IN(0,1)),
	FOREIGN KEY(`id_Prestamo`) REFERENCES `prestamos`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `monedas` (
	`id`	INTEGER NOT NULL,
	`Nombre`	TEXT NOT NULL,
	`Simbolo`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `ingresos` (
	`id`	INTEGER NOT NULL,
	`id_Transaccion`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Transaccion`) REFERENCES `transacciones`(`id`)
);
CREATE TABLE IF NOT EXISTS `historial_presupuesto` (
	`id`	INTEGER NOT NULL,
	`Saldo`	REAL NOT NULL,
	`id_Presupuesto`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Presupuesto`) REFERENCES `presupuestos`(`id`)
);
CREATE TABLE IF NOT EXISTS `egresos` (
	`id`	INTEGER NOT NULL,
	`id_Transaccion`	INTEGER NOT NULL,
	FOREIGN KEY(`id_Transaccion`) REFERENCES `transacciones`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `cuentas` (
	`id`	INTEGER NOT NULL,
	`Saldo`	REAL NOT NULL,
	`Nombre`	TEXT NOT NULL,
	`Descripcion`	TEXT,
	`id_Usuario`	TEXT NOT NULL,
	`id_Tipocuenta`	INTEGER NOT NULL,
	`id_Moneda`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Moneda`) REFERENCES `monedas`(`id`),
	FOREIGN KEY(`id_Usuario`) REFERENCES `usuarios`(`id`),
	FOREIGN KEY(`id_Tipocuenta`) REFERENCES `tipocuenta`(`id`)
);
CREATE TABLE IF NOT EXISTS `creditos` (
	`id`	INTEGER NOT NULL,
	`Fecha_Pago`	TEXT NOT NULL,
	`Limite`	REAL NOT NULL,
	`id_Cuenta`	INTEGER NOT NULL,
	FOREIGN KEY(`id_Cuenta`) REFERENCES `cuentas`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE IF NOT EXISTS `cheques` (
	`id`	INTEGER NOT NULL,
	`Valor`	REAL NOT NULL,
	`Fecha`	TEXT NOT NULL,
	`id_Cuenta`	INTEGER NOT NULL,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`id_Cuenta`) REFERENCES `cuentas`(`id`)
);
CREATE TABLE IF NOT EXISTS `categorias` (
	`id`	INTEGER NOT NULL,
	`Nombre`	TEXT NOT NULL,
	PRIMARY KEY(`id`)
);
COMMIT;
