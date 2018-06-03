#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, SelectField, HiddenField, DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length,  InputRequired
from Proyecto.modelos import Usuarios, Cuentas

class LoginForm(FlaskForm):
	username = StringField('Usuario', validators=[DataRequired(),])
	password = PasswordField('Clave', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	name = StringField('Nombre', validators=[DataRequired()])
	username = StringField('Usuario', validators=[DataRequired(), Length(min=4, message= 'Nombre de usuario debe contener más de 4 caracteres.'.decode('utf-8')), Length(max=20, message= 'Nombre de usuario debe contener menos de 20 caracteres.')])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Contraseña'.decode('utf-8'), validators=[DataRequired(), Length(min=4, message= 'Contraseña debe contener más de 4 caracteres.'.decode('utf-8')), Length(max=20, message= 'Contraseña debe contener menos de 20 caracteres.'.decode('utf-8'))])
	password2 = PasswordField('Repite Contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	
	def validate_username(self, username):
		user = Usuarios.query.filter_by(Usuario=username.data).first()
		if user is not None:
			raise ValidationError('Nombre de usuario no disponible.')

	def validate_email(self, email):
		user = Usuarios.query.filter_by(Correo=email.data).first()
		if user is not None:
			raise ValidationError('Por favor utilice otra dirección de correo electrónico.'.decode('utf-8'))

class CuentaForm(FlaskForm):
	nombre = StringField('Nombre', validators=[DataRequired()])
	saldo = DecimalField('Saldo', validators=[DataRequired()])
	descripcion = StringField('Descripcion')
	categoria = SelectField('Categoria', choices=[('1','Efectivo'),('2','Crédito'.decode('utf-8')),('3','Cheques'),('4','Préstamo'.decode('utf-8'))], validators=[DataRequired(message= 'Seleccione una categoría.'.decode('utf-8'))])
	moneda = SelectField('Moneda', choices=[('AFN','Afganí Afgano'.decode('utf-8')),('PAB','Balboa'),('BTC','BitCoin'),('VEF','Bolívar Fuerte'.decode('utf-8')),('BOB','Boliviano'),('KES','Chelín Keniano'.decode('utf-8')),('CRC','Colón Costarricense'.decode('utf-8')),('SVC','Colón Salvadoreño'.decode('utf-8')),('CZK','Corona Checa'),('DKK','Corona Danesa'),('ISK','Corona Islandesa'),('SEK','Corona Sueca'),('MKD','Denar Macedonio'),('DZD','Dinar Algerino'),('TND','Dinar Tuniso'),('IQD','Dinar Iraquí'.decode('utf-8')),('JOD','Dinar Jordano'),('LYD','Dinar Libio'),('RSD','Dinar Serbio'),('MAD','Dirham Marroquí'.decode('utf-8')),('AED','Dirham de los Emiratos Árabes Unidos'.decode('utf-8')),('AUD','Dólar Australiano'.decode('utf-8')),('CAD','Dólar Canadiense'.decode('utf-8')),('USD','Dólar Estadounidense'.decode('utf-8')),('GYD','Dólar Guyanés'.decode('utf-8')),('JMD','Dólar Jamaiquino'.decode('utf-8')),('LRD','Dólar Liberiano'.decode('utf-8')),('SRD','Dólar Surinamés'.decode('utf-8')),('BBD','Dólar de Barbados'.decode('utf-8')),('HKD','Dólar de Hong Kong'.decode('utf-8')),('NZD','Dólar Neozelandés'.decode('utf-8')),('SGD','Dólar de Singapur'.decode('utf-8')),('TTD','Dólar Trinitense'.decode('utf-8')),('KYD','Dólar de las Islas Caimán'.decode('utf-8')),('AMD','Dram Armenio'),('EUR','Euro'),('ANG','Florín Antillano Neerlandés'.decode('utf-8')),('AWG','Florín Arubeño'.decode('utf-8')),('HUF','Florinto Húngaro'.decode('utf-8')),('CHF','Franco Suizo'),('HTG','Gourde Haitiano'),('UAH','Grivna Ucraniana'),('PYG','Guaraní'.decode('utf-8')),('LAK','Kip Laosiano'),('NOK','Krone Noruego'),('HRK','Kuna Croata'),('AOA','Kwanza Angoleño'.decode('utf-8')),('ALL','Lek Albanés'.decode('utf-8')),('HNL','Lempira Hondureño'.decode('utf-8')),('MDL','Leu Moldavo'),('RON','Leu Rumano'),('BGN','Lev Búlgaro'.decode('utf-8')),('EGP','Libra Egipcia'),('AED','Libra Esterlina'),('LBP','Libra Libanesa'),('SYP','Libra Siria'),('SDG','Libra Sudanesa'),('TRY','Libra Turca'),('AZN','Manat Azerbaiyano'),('BAM','Marco Bosnioherzegovino'),('NGN','Naira Nigeriana'),('BYN','Nuevo Rublo Bielorruso'),('ILS','Nuevo Séquel Israelí'.decode('utf-8')),('PEN','Sol Peruano'),('ARS','Peso Argentino'),('CLP','Peso Chileno'),('COP','Peso Colombiano'),('CUP','Peso Cubano'),('CUC','Peso Cubano Convertible'),('DOP','Peso Dominicano'),('PHP','Peso Filipino'),('MXN','Peso Mexicano'),('UYU','Peso Uruguayo'),('GTQ','Quetzal'),('ZAR','Rand Sudafricano'),('BRL','Real Brasileño'.decode('utf-8')),('YER','Rial Yemení'.decode('utf-8')),('KHR','Riel Kamboyano'),('MYR','Ringgit Malayo'),('SAR','Riyal Saudí'.decode('utf-8')),('RUB','Rublo Ruso'),('INR','Rupia India'),('IDR','Rupia de Indonesia'),('PKR','Rupia Pakistaní'.decode('utf-8')),('MVR','Rupia de Maldivas'),('NRP','Rupia de Nepal'),('LKR','Rupia de Sri Lanka'),('BDT','Taka Bangladesí'.decode('utf-8')),('MNT','Tugrik Mongol'),('KPW','Won Norcoreano'),('KRW','Won Surcoreano'),('JPY','Yen'),('CNY','Yuan')], default='COP')
	submit = SubmitField('CREAR')

class EditarNombre(FlaskForm):
	nombre = StringField('Nombre', validators=[DataRequired()])
	submit = SubmitField('Aceptar')

class EditarUsuario(FlaskForm):
	usuario = StringField('Usuario', validators=[DataRequired(), Length(min=4, message= 'Nombre de usuario debe contener más de 4 caracteres.'.decode('utf-8')), Length(max=20, message= 'Nombre de usuario debe contener menos de 20 caracteres.')])
	submit = SubmitField('Aceptar')
	
	def validate_usuario(self, usuario):
		user = Usuarios.query.filter_by(Usuario=usuario.data).first()
		if user is not None:
			raise ValidationError('Nombre de usuario no disponible.')
			
class EditarCorreo(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(message='Dirección de correo electrónico no válida.'.decode('utf-8'))])
	submit = SubmitField('Aceptar')
	
	def validate_email(self, email):
		user = Usuarios.query.filter_by(Correo=email.data).first()
		if user is not None:
			raise ValidationError('Por favor utilice otra dirección de correo electrónico.'.decode('utf-8'))

class EditarClave(FlaskForm):
	passwordactual = PasswordField('Contraseña'.decode('utf-8'), validators=[DataRequired()])
	password = PasswordField('Contraseña'.decode('utf-8'), validators=[DataRequired(), Length(min=4, message= 'Contraseña debe contener más de 4 caracteres.'.decode('utf-8')), Length(max=20, message= 'Contraseña debe contener menos de 20 caracteres.'.decode('utf-8'))])
	password2 = PasswordField('Repite Contraseña', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Aceptar') 

class CreditoForm(FlaskForm):
	fecha_pago = StringField('Fecha_Pago', validators=[DataRequired()])
	limite = DecimalField('Limite', validators=[DataRequired()])
	submit = SubmitField('Crear')

class ChequeForm(FlaskForm):
	valor = DecimalField('Valor', validators=[DataRequired()])
	fecha = StringField('Fecha', validators=[DataRequired()])
	submit = SubmitField('Crear')
	
class PrestamoForm(FlaskForm):
	valor = DecimalField('Valor_Prestamo', validators=[DataRequired()])
	cuotas = IntegerField('Cuotas', validators=[DataRequired()])
	TAE = DecimalField('TAE', validators=[DataRequired()])
	fecha_pago = StringField('Fecha_Pago', validators=[DataRequired()])
	submit = SubmitField('Crear')

class TransaccionForm(FlaskForm):
	fecha = StringField('Fecha', validators=[DataRequired()])
	valor = DecimalField('Valor', validators=[DataRequired()])
	descripcion = StringField('Descripcion')
	tipo = SelectField('Tipo', choices=[('1','Ingreso'),('2','Egreso'),('3','Transferencia')], validators=[DataRequired(message= 'Seleccione un tipo')])
	submit = SubmitField('Crear')

class TransferenciaForm(FlaskForm):
	Cuenta_Destino = HiddenField('Cuenta_Destino', validators=[DataRequired()])
	submit = SubmitField('Crear')