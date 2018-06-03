from datetime import datetime
from Proyecto import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from Proyecto import login

class Usuarios(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Nombre = db.Column(db.Text, nullable=False)
	Usuario = db.Column(db.Text, nullable=False)
	Correo = db.Column(db.Text, nullable=False)
	Clave = db.Column(db.Text, nullable=False)
	Cuentas_Relacion = db.relationship('Cuentas', backref='Usuario')
	
	def set_password(self, password):
		self.Clave = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.Clave, password)

	def __repr__(self):
		return '<Usuarios {}>'.format(self.Nombre)
	
@login.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))
	
class Tipocuenta(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Nombre = db.Column(db.Text, nullable=False)
	Cuentas_Relacion = db.relationship('Cuentas', backref='Tipo')
	
	def __repr__(self):
		return '<Tipocuenta {}>'.format(self.Nombre)
	
class Cuentas(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Saldo = db.Column(db.REAL, nullable=True)
	Saldo_COP = db.Column(db.Integer, nullable=False)
	Nombre = db.Column(db.Text, nullable=False)
	Logo = db.Column(db.Integer, nullable=False)
	#Llaves Foraneas
	#Estado = db.Column(db.Boolean, nullable=False)
	Descripcion = db.Column(db.Text)
	id_Usuario = db.Column(db.Text, db.ForeignKey('usuarios.id'), nullable=False)
	id_Tipocuenta = db.Column(db.Integer, db.ForeignKey('tipocuenta.id'), nullable=False)
	id_Moneda = db.Column(db.Integer, db.ForeignKey('monedas.id'), nullable=False)
	#id_Logo = db.Column(db.Integer, db.ForeignKey('logos.id'), nullable=True) #, nullable=False)
	#Relaciones
	Creditos_Relacion = db.relationship('Creditos', backref='Cuenta')
	Cheques_Relacion = db.relationship('Cheques', backref='Cuenta')
	Prestamos_Relacion = db.relationship('Prestamos', backref='Cuenta')
	Transacciones_Relacion = db.relationship('Transacciones', backref='Cuenta')
	Presupuesto_cuenta_Relacion = db.relationship('Presupuesto_cuenta', backref='Cuenta')
	Transferencias_Relacion = db.relationship('Transferencias', backref='Cuenta')
	
	def __repr__(self):
		return '<Cuentas {}>'.format(self.Nombre)
		
'''class Logos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	URL = db.Column(db.Text, nullable=False)
	#Estado = db.Column(db.Text, nullable=False)
	Cuentas_Relacion = db.relationship('Cuentas', backref='Logo')
	Presupuestos_Relacion = db.relationship('Presupuestos', backref='Logo')
	
	def __repr__(self):
		return '<Logos {}>'.format(self.URL)'''
	
class Monedas(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Nombre = db.Column(db.Text, nullable=False)
	Simbolo = db.Column(db.Text, nullable=False)
	Cuentas_Relacion = db.relationship('Cuentas', backref='Moneda')
	Presupuestos_Relacion = db.relationship('Presupuestos', backref='Moneda')
	
	def __repr__(self):
		return '<Monedas {}>'.format(self.Nombre)

class Creditos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Fecha_Pago = db.Column(db.Text, nullable=False)
	Limite = db.Column(db.REAL, nullable=True)
	Limite_COP = db.Column(db.Integer, nullable=False)
	#Estado = db.Column(db.Text, nullable=False)
	id_Cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)

class Cheques(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Valor = db.Column(db.REAL, nullable=True)
	Valor_COP = db.Column(db.Integer, nullable=False)
	Fecha = db.Column(db.Text, nullable=False)
	id_Cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
	Reembolsos_Relacion = db.relationship('Reembolsos', backref='Cheque')

class Prestamos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	TAE = db.Column(db.REAL, nullable=False)
	Cuotas = db.Column(db.Integer, nullable=False)
	Valor_Prestamo = db.Column(db.REAL, nullable=True)
	Valor_Prestamo_COP = db.Column(db.Integer, nullable=False)
	id_Cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
	Pago_prestamo_Relacion = db.relationship('Pago_prestamo', backref='Prestamo')
	
class Pago_prestamo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Dia_Pago = db.Column(db.Text, nullable=False)
	Pago_Completo = db.Column(db.Boolean, nullable=False)
	Valor_Pagar = db.Column(db.REAL, nullable=True)
	Valor_Pagar_COP = db.Column(db.Integer, nullable=False)
	id_Prestamo = db.Column(db.Integer, db.ForeignKey('prestamos.id'), nullable=False)
	
class Categorias(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Nombre = db.Column(db.Text, nullable=False)
	Presupuestos_Relacion = db.relationship('Presupuestos', backref='Categoria')
	
	def __repr__(self):
		return '<Categorias {}>'.format(self.Nombre)
		
class Presupuestos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Saldo = db.Column(db.REAL, nullable=False)
	Nombre = db.Column(db.Text, nullable=False)
	Estado = db.Column(db.Boolean, nullable=False)
	id_Categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
	#id_Logo = db.Column(db.Integer, db.ForeignKey('logos.id'), nullable=False)
	id_Moneda = db.Column(db.Integer, db.ForeignKey('monedas.id'), nullable=False)
	Historial_presupuesto_Relacion = db.relationship('Historial_presupuesto', backref='Presupuesto')
	Presupuesto_cuenta_Relacion = db.relationship('Presupuesto_cuenta', backref='Presupuesto')
	
	def __repr__(self):
		return '<Presupuestos {}>'.format(self.Nombre)

class Historial_presupuesto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Saldo = db.Column(db.REAL, nullable=False)
	id_Presupuesto = db.Column(db.Integer, db.ForeignKey('presupuestos.id'), nullable=False)

transaccion_presupuesto_cuenta = db.Table('transaccion_presupuesto_cuenta', db.Column('id_Transaccion', db.Integer, db.ForeignKey('transacciones.id')), db.Column('id_Presupuesto_cuenta', db.Integer, db.ForeignKey('presupuesto_cuenta.id')))

class Transacciones(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Fecha = db.Column(db.Text, nullable=False)
	Valor = db.Column(db.REAL, nullable=True)
	Valor_COP = db.Column(db.Integer, nullable=False)
	Tipo = db.Column(db.Text, nullable=False)
	Descripcion = db.Column(db.Text)
	id_Cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
	
	Transaccion_Presupuesto_Cuenta_Relacion= db.relationship('Presupuesto_cuenta', secondary='transaccion_presupuesto_cuenta', backref=db.backref('Transacciones', lazy='dynamic'))
	Ingresos_Relacion = db.relationship('Ingresos', backref='Transaccion')
	Egresos_Relacion = db.relationship('Egresos', backref='Transaccion')
	Reembolsos_Relacion = db.relationship('Reembolsos', backref='Transaccion')
	Transferencias_Relacion = db.relationship('Transferencias', backref='Transaccion')
	
class Presupuesto_cuenta(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_Cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
	id_Presupuesto = db.Column(db.Integer, db.ForeignKey('presupuestos.id'), nullable=False)

class Reembolsos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_Cheque = db.Column(db.Integer, db.ForeignKey('cheques.id'), nullable=False)
	id_Transaccion = db.Column(db.Integer, db.ForeignKey('transacciones.id'), nullable=False)
	
class Transferencias(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_Transaccion = db.Column(db.Integer, db.ForeignKey('transacciones.id'), nullable=False)
	id_CuentaDestino = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)