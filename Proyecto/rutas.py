#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, session, jsonify, json
from Proyecto import app, db #app es la variable de __init__.py que es parte de la carpeta Proyecto, db es la base de datos
from Proyecto.forms import LoginForm, RegistrationForm, CuentaForm, EditarNombre, EditarUsuario, EditarCorreo, EditarClave, CreditoForm, ChequeForm, PrestamoForm, TransaccionForm, TransferenciaForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from Proyecto.modelos import Usuarios, Cuentas, Tipocuenta, Monedas, Creditos, Cheques, Prestamos, Pago_prestamo, Transacciones, Transferencias
from openexchangerates.exchange import Exchange #Moneda
import datetime

exchange= Exchange()

@app.route('/')
@app.route('/index')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('principal'))
	users = Usuarios.query.all()
	return render_template('index.html', users=users)

@app.route('/acceso')
def acceso():
	users = Usuarios.query.all()
	if len(users) == 2:
		return redirect(url_for('login'))
	if current_user.is_authenticated:
		return redirect(url_for('principal'))
	user = Usuarios.query.filter_by(Usuario='a').first()
	login_user(user)
	return redirect(url_for('principal'))
	
@app.route('/404')
def trabajando():
	return render_template('trabajando.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('principal'))
	form = LoginForm()
	users = Usuarios.query.all()																											
	return render_template('login.html', form=form, users=users)

@app.route('/LoginAjaxProcess', methods=['GET', 'POST'])
def LoginAjaxProcess():
	if request.method == 'GET':
		return redirect(url_for('login'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuarios.query.filter_by(Usuario=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			return json.dumps('nohay')
		else:
			session['Login']=form.username.data
			return json.dumps('si')
	return json.dumps(form.errors)

@app.route('/LoginAjaxDone')
def LoginAjaxDone():
	if 'Login' in session:
		Login=session['Login']
		user = Usuarios.query.filter_by(Usuario=Login).first()
		login_user(user)
		session.pop('Login', None)
		return redirect(url_for('principal'))
	else:
		return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/DeleteProfile')
@login_required
def DeleteProfile():
	#Eliminar transacciones
	usuario=current_user
	cuentas = Cuentas.query.all()
	for cuenta in cuentas:
		if cuenta.id_Tipocuenta == 1:
			#Efectivo
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 2:
			#Credito
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
			db.session.delete(credito)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 3:
			#Cheque
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
			for cheque in cheques:
				if cheque is not None:
					db.session.delete(cheque)
					db.session.commit()
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 4:
			#Prestamo
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
			pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
			db.session.delete(pago_prestamo)
			db.session.delete(prestamo)
			db.session.delete(cuenta)
			db.session.commit()
	db.session.delete(usuario)
	db.session.commit()
	logout_user()
	flash('Su perfil y cuentas han sido eliminados.')
	return redirect(url_for('index'))
	
@app.route('/DeleteAccounts')
@login_required
def DeleteAccounts():
	#Eliminar transacciones
	cuentas = Cuentas.query.all()
	for cuenta in cuentas:
		if cuenta.id_Tipocuenta == 1:
			#Efectivo
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 2:
			#Credito
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
			db.session.delete(credito)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 3:
			#Cheque
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
			for cheque in cheques:
				if cheque is not None:
					db.session.delete(cheque)
					db.session.commit()
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 4:
			#Prestamo
			transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
			for transaccion in transacciones:
				if transaccion is not None:
					transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
					for transferencia in transferencias:
						if transferencia is not None:
							db.session.delete(transferencia)
							db.session.commit()
					db.session.delete(transaccion)
					db.session.commit()
			prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
			pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
			db.session.delete(pago_prestamo)
			db.session.delete(prestamo)
			db.session.delete(cuenta)
			db.session.commit()
	flash('Sus cuentas han sido eliminadas.')
	return redirect(url_for('principal'))
	
@app.route('/EditProfile', methods=['GET','POST'])
@login_required
def EditProfile():
	user=current_user
	if user.Usuario == 'a':
		return redirect(url_for('principal'))
	else:
		formnombre = EditarNombre(prefix='a')
		formusuario = EditarUsuario(prefix='b')
		formcorreo = EditarCorreo(prefix='c')
		formclave = EditarClave(prefix='d')
	return render_template('editarperfil.html', formnombre=formnombre, formusuario=formusuario, formcorreo=formcorreo, formclave=formclave, user=user)

@app.route('/EditProfile/NameAjaxProcess', methods=['GET', 'POST'])
@login_required
def NameAjaxProcess():
	usuario=current_user
	if request.method == 'GET':
		return redirect(url_for('EditProfile'))
	formnombre = EditarNombre(prefix='a')
	if formnombre.validate_on_submit():
		if formnombre.nombre.data == usuario.Nombre:
			return json.dumps('igual')
		else:
			session['NombreNuevo'] = formnombre.nombre.data
			return json.dumps('si')
		#return jsonify(data=(formnombre.nombre.data)) --> jsonify entrega diccionario
	#return jsonify(data=formnombre.errors)
	return json.dumps('no')
	
@app.route('/EditProfile/NameAjaxDone')
@login_required
def NameAjaxDone():
	if 'NombreNuevo' in session:
		NombreNuevo=session['NombreNuevo']
		usuario=Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Nombre=NombreNuevo
		db.session.commit()
		session.pop('NombreNuevo', None)
		flash('Nombre cambiado.')
		return redirect(url_for('EditProfile'))
	else:
		return redirect(url_for('EditProfile'))

@app.route('/EditProfile/UserAjaxProcess', methods=['GET', 'POST'])
@login_required
def UserAjaxProcess():
	usuario=current_user
	if request.method == 'GET':
		return redirect(url_for('EditProfile'))
	formusuario = EditarUsuario(prefix='b')
	if formusuario.validate_on_submit():
		if formusuario.usuario.data == usuario.Usuario:
			return json.dumps('igual')
		username = Usuarios.query.filter_by(Usuario=formusuario.usuario.data).first()
		if username is not None:
			return json.dumps('nodisponible')
		else:
			session['UsuarioNuevo'] = formusuario.usuario.data
			return json.dumps('si')
	return json.dumps('no')
	
@app.route('/EditProfile/UserAjaxDone')
@login_required
def UserAjaxDone():
	if 'UsuarioNuevo' in session:
		UsuarioNuevo=session['UsuarioNuevo']
		usuario=Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Usuario=UsuarioNuevo
		db.session.commit()
		session.pop('UsuarioNuevo', None)
		flash('Usuario cambiado.')
		return redirect(url_for('EditProfile'))
	else:
		return redirect(url_for('EditProfile'))
		
@app.route('/EditProfile/EmailAjaxProcess', methods=['GET', 'POST'])
@login_required
def EmailAjaxProcess():
	usuario=current_user
	if request.method == 'GET':
		return redirect(url_for('EditProfile'))
	formcorreo = EditarCorreo(prefix='c')
	if formcorreo.validate_on_submit():
		if formcorreo.email.data == usuario.Correo:
			return json.dumps('igual')
		correo = Usuarios.query.filter_by(Correo=formcorreo.email.data).first()
		if correo is not None:
			return json.dumps('nodisponible')
		else:
			session['CorreoNuevo'] = formcorreo.email.data
			return json.dumps('si')
	return json.dumps(formcorreo.email.errors)
	
@app.route('/EditProfile/EmailAjaxDone')
@login_required
def EmailAjaxDone():
	if 'CorreoNuevo' in session:
		CorreoNuevo=session['CorreoNuevo']
		usuario=Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Correo=CorreoNuevo
		db.session.commit()
		session.pop('CorreoNuevo', None)
		flash('Correo cambiado.')
		return redirect(url_for('EditProfile'))
	else:
		return redirect(url_for('EditProfile'))
		
@app.route('/EditProfile/ClaveAjaxProcess', methods=['GET', 'POST'])
@login_required
def ClaveAjaxProcess():
	if request.method == 'GET':
		return redirect(url_for('EditProfile'))
	formclave = EditarClave(prefix='d')
	if formclave.validate_on_submit():
		usuario= Usuarios.query.filter_by(id=current_user.id).first()
		if usuario.check_password(formclave.passwordactual.data) == True:
			if formclave.password.data == formclave.passwordactual.data:
				return json.dumps('igual')
			else:
				session['ClaveNueva'] = formclave.password.data
				return json.dumps('si')
		else:
			return json.dumps('no')
	return json.dumps(formclave.errors)
	
@app.route('/EditProfile/ClaveAjaxDone')
@login_required
def ClaveAjaxDone():
	if 'ClaveNueva' in session:
		ClaveNueva=session['ClaveNueva']
		usuario=Usuarios.query.filter_by(id=current_user.id).first()
		usuario.set_password(ClaveNueva)
		db.session.commit()
		session.pop('ClaveNueva', None)
		flash('Contraseña cambiada.'.decode('utf-8'))
		return redirect(url_for('EditProfile'))
	else:
		return redirect(url_for('EditProfile'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
	users = Usuarios.query.all()
	if current_user.is_authenticated:
		user=current_user
		if user.Usuario != 'a':
			return redirect(url_for('principal'))
	form = RegistrationForm()
	return render_template('registro.html', form=form, users=users)

@app.route('/RegistroAjaxProcess', methods=['GET', 'POST'])
def RegistroAjaxProcess():
	if request.method == 'GET':
		return redirect(url_for('registro'))
	form = RegistrationForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			session['NuevoRegistro']={'Nombre':form.name.data, 'Usuario':form.username.data, 'Correo':form.email.data, 'Clave':form.password.data}
			return json.dumps('si')
		else:
			usuario= Usuarios.query.filter_by(Usuario='a').first()
			login_user(usuario)
			session['NuevoRegistro']={'Nombre':form.name.data, 'Usuario':form.username.data, 'Correo':form.email.data, 'Clave':form.password.data}
			return json.dumps('si')
	#return json.dumps(formclave.errors)
	return json.dumps(form.errors)

@app.route('/RegistroAjaxDone')
def RegistroAjaxDone():
	if 'NuevoRegistro' in session:
		NuevoRegistro=session['NuevoRegistro']
		user= Usuarios(Nombre=NuevoRegistro['Nombre'], Usuario=NuevoRegistro['Usuario'], Correo=NuevoRegistro['Correo'])
		user.set_password(NuevoRegistro['Clave'])
		db.session.add(user)
		db.session.commit()
		session.pop('NuevoRegistro', None)
		logout_user()
		flash('Registro Exitoso.', 'registroexitoso')
		return redirect(url_for('login'))
	else:
		return redirect(url_for('registro'))
	
@app.route('/principal')
@login_required
def principal():
	user=current_user
	return render_template('principal.html', user=user)

@app.route('/principal/cuentas')
@login_required
def cuentas():
	cuentas= Cuentas.query.all()
	monedas= Monedas.query.all()
	return render_template('cuentas.html', cuentas=cuentas, monedas=monedas)

@app.route('/principal/cuentas/AddCuenta', methods=['GET', 'POST'])
@login_required
def AddCuenta():
	usuario=current_user
	cuentaform = CuentaForm(prefix='a')
	creditoform = CreditoForm(prefix='b')
	prestamoform = PrestamoForm(prefix='c')
	'''if form.validate_on_submit():
		cuenta= Cuentas.query.filter_by(Nombre=form.nombre.data).first()
		moneda= Monedas.query.filter_by(Simbolo=form.moneda.data).first()
		if cuenta is not None:
			flash('Ya tienes una cuenta con ese nombre.')
			return redirect(url_for('AddCuenta'))
					
			elif form.categoria.data == '4':
				if moneda.id == 67:
					logoform = request.form.get("oculto", None)
					cuentanueva= {'Saldo_COP':str(int(form.saldo.data)), 'Nombre':form.nombre.data, 'Logo':logoform, 'Descripcion':form.descripcion.data, 'id_Usuario':usuario.id, 'id_Tipocuenta':'4', 'id_Moneda':moneda.id}
					session['cuentanuevaprestamo']=cuentanueva
					return redirect(url_for('prestamo'))
				else:
					saldo_cop= exchange.exchange(float(form.saldo.data), moneda.Simbolo, 'COP')
					saldo_cop= round(saldo_cop)
					logoform = request.form.get("oculto", None)
					cuentanueva= {'Saldo':str(form.saldo.data), 'Saldo_COP':str(int(saldo_cop)), 'Nombre':form.nombre.data, 'Logo':logoform, 'Descripcion':form.descripcion.data, 'id_Usuario':usuario.id, 'id_Tipocuenta':'4', 'id_Moneda':moneda.id}
					session['cuentanuevaprestamo']=cuentanueva
					return redirect(url_for('prestamo'))'''
	return render_template('nuevacuenta.html', CuentaForm=cuentaform, CreditoForm=creditoform, PrestamoForm=prestamoform)

@app.route('/principal/cuentas/AddCuentaAjaxProcess', methods=['GET', 'POST'])
@login_required
def AddCuentaAjaxProcess():
	usuario= current_user
	if request.method == 'GET':
		return redirect(url_for('AddCuenta'))
	cuentaform = CuentaForm(prefix='a')
	if cuentaform.validate_on_submit:
		#Validaciones extras
		if cuentaform.saldo.data is None:
			if len(cuentaform.nombre.data) == 0:
				return json.dumps('llenarambos')
			else:
				return json.dumps('llenarsaldo')
		else:
			if len(cuentaform.nombre.data) == 0:
				return json.dumps('llenarnombre')
			else:
				cuenta= Cuentas.query.filter_by(Nombre=cuentaform.nombre.data).first()
				moneda= Monedas.query.filter_by(Simbolo=cuentaform.moneda.data).first()
				if cuenta is not None:
					return json.dumps('yaexiste')
		#Paso
				else:
					#-----------Efectivo-------#
					if cuentaform.categoria.data == '1':
						logocuenta = request.form.get("oculto", None)
						if moneda.id == 67:
							session['cuentanuevaefectivo']={'Saldo_COP':str(int(cuentaform.saldo.data)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'1', 'id_Moneda':moneda.id}
							return json.dumps('valido')
						else:
							saldo_cop= exchange.exchange(float(cuentaform.saldo.data), moneda.Simbolo, 'COP')
							saldo_cop= round(saldo_cop)
							session['cuentanuevaefectivo']={'Saldo':str(float(cuentaform.saldo.data)), 'Saldo_COP':str(int(saldo_cop)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'1', 'id_Moneda':moneda.id}
							return json.dumps('valido')
					#--------------------------#	
					#---------------Credito----#
					elif cuentaform.categoria.data == '2':
						logocuenta = request.form.get("oculto", None)
						if moneda.id == 67:
							session['cuentanuevacredito']={'Saldo_COP':str(int(cuentaform.saldo.data)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'2', 'id_Moneda':moneda.id}
							return json.dumps({'Tipo':'credito', 'Datos':session['cuentanuevacredito'], 'Moneda':moneda.Nombre, 'Simbolo':moneda.Simbolo})
						else:
							saldo_cop= exchange.exchange(float(cuentaform.saldo.data), moneda.Simbolo, 'COP')
							saldo_cop= round(saldo_cop)
							session['cuentanuevacredito']={'Saldo':str(float(cuentaform.saldo.data)), 'Saldo_COP':str(int(saldo_cop)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'2', 'id_Moneda':moneda.id}
							return json.dumps({'Tipo':'credito', 'Datos':session['cuentanuevacredito'], 'Moneda':moneda.Nombre, 'Simbolo':moneda.Simbolo})
					#---------------Cheque----#
					elif cuentaform.categoria.data == '3':
						logocuenta = request.form.get("oculto", None)
						if moneda.id == 67:
							session['cuentanuevacheque']={'Saldo_COP':str(int(cuentaform.saldo.data)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'3', 'id_Moneda':moneda.id}
							return json.dumps('valido')
						else:
							saldo_cop= exchange.exchange(float(cuentaform.saldo.data), moneda.Simbolo, 'COP')
							saldo_cop= round(saldo_cop)
							session['cuentanuevacheque']={'Saldo':str(float(cuentaform.saldo.data)), 'Saldo_COP':str(int(saldo_cop)), 'Nombre':cuentaform.nombre.data, 'Logo':logocuenta, 'Descripcion':cuentaform.descripcion.data, 'id_Usuario': usuario.id, 'id_Tipocuenta':'3', 'id_Moneda':moneda.id}
							return json.dumps('valido')
					#-------------Prestamo-----#
					elif cuentaform.categoria.data == '4':
						logocuenta = request.form.get("oculto", None)
						if moneda.id == 67:
							session['cuentanuevaprestamo']={'Nombre':cuentaform.nombre.data, 'Saldo_COP':str(int(cuentaform.saldo.data)), 'Descripcion':cuentaform.descripcion.data, 'Logo':logocuenta, 'id_Usuario': usuario.id, 'id_Tipocuenta':'4', 'id_Moneda': moneda.id, 'Moneda':{'id':moneda.id, 'Nombre':moneda.Nombre, 'Simbolo':moneda.Simbolo}}
							return json.dumps({'Tipo':'prestamo', 'Datos':session['cuentanuevaprestamo']})
						else:
							saldo_cop= exchange.exchange(float(cuentaform.saldo.data), moneda.Simbolo, 'COP')
							saldo_cop= round(saldo_cop)
							session['cuentanuevaprestamo']={'Nombre':cuentaform.nombre.data, 'Saldo':str(float(cuentaform.saldo.data)), 'Saldo_COP':str(int(saldo_cop)), 'Descripcion':cuentaform.descripcion.data, 'Logo':logocuenta, 'id_Usuario': usuario.id, 'id_Tipocuenta':'4', 'id_Moneda': moneda.id, 'Moneda':{'id':moneda.id, 'Nombre':moneda.Nombre, 'Simbolo':moneda.Simbolo}}
							return json.dumps({'Tipo':'prestamo', 'Datos':session['cuentanuevaprestamo']})
	return json.dumps('no')

@app.route('/principal/cuentas/AddCuentaAjaxDone')
@login_required
def AddCuentaAjaxDone():
	if 'cuentanuevaefectivo' in session:
		cuentanuevaefectivo=session['cuentanuevaefectivo']
		if cuentanuevaefectivo['id_Moneda'] == 67:
			cuenta= Cuentas(Nombre=cuentanuevaefectivo['Nombre'], Saldo_COP=cuentanuevaefectivo['Saldo_COP'], Logo=cuentanuevaefectivo['Logo'], Descripcion=cuentanuevaefectivo['Descripcion'], id_Usuario=cuentanuevaefectivo['id_Usuario'], id_Tipocuenta=cuentanuevaefectivo['id_Tipocuenta'], id_Moneda=cuentanuevaefectivo['id_Moneda'])
			db.session.add(cuenta)
			db.session.commit()
			session.pop('cuentanuevaefectivo', None)
			return redirect(url_for('cuentas'))
		else:
			cuenta= Cuentas(Nombre=cuentanuevaefectivo['Nombre'], Saldo=cuentanuevaefectivo['Saldo'], Saldo_COP=cuentanuevaefectivo['Saldo_COP'], Logo=cuentanuevaefectivo['Logo'], Descripcion=cuentanuevaefectivo['Descripcion'], id_Usuario=cuentanuevaefectivo['id_Usuario'], id_Tipocuenta=cuentanuevaefectivo['id_Tipocuenta'], id_Moneda=cuentanuevaefectivo['id_Moneda'])
			db.session.add(cuenta)
			db.session.commit()
			session.pop('cuentanuevaefectivo', None)
			return redirect(url_for('cuentas'))
	if 'cuentanuevacheque' in session:
		cuentanuevacheque=session['cuentanuevacheque']
		if cuentanuevacheque['id_Moneda'] == 67:
			cuenta= Cuentas(Nombre=cuentanuevacheque['Nombre'], Saldo_COP=cuentanuevacheque['Saldo_COP'], Logo=cuentanuevacheque['Logo'], Descripcion=cuentanuevacheque['Descripcion'], id_Usuario=cuentanuevacheque['id_Usuario'], id_Tipocuenta=cuentanuevacheque['id_Tipocuenta'], id_Moneda=cuentanuevacheque['id_Moneda'])
			db.session.add(cuenta)
			db.session.commit()
			session.pop('cuentanuevacheque', None)
			return redirect(url_for('cuentas'))
		else:
			cuenta= Cuentas(Nombre=cuentanuevacheque['Nombre'], Saldo=cuentanuevacheque['Saldo'], Saldo_COP=cuentanuevacheque['Saldo_COP'], Logo=cuentanuevacheque['Logo'], Descripcion=cuentanuevacheque['Descripcion'], id_Usuario=cuentanuevacheque['id_Usuario'], id_Tipocuenta=cuentanuevacheque['id_Tipocuenta'], id_Moneda=cuentanuevacheque['id_Moneda'])
			db.session.add(cuenta)
			db.session.commit()
			session.pop('cuentanuevaefectivo', None)
			return redirect(url_for('cuentas'))
	return redirect(url_for('AddCuenta'))	

@app.route('/principal/cuentas/AddCuenta/CreditoAjaxProcess', methods=['GET', 'POST'])
@login_required
def CreditoAjaxProcess():
	if request.method == 'GET':
		return redirect(url_for('AddCuenta'))
	creditoform = CreditoForm(prefix='b')
	if creditoform.validate_on_submit():
		if 'cuentanuevacredito' in session:
			cuentanuevacredito=session['cuentanuevacredito']
			moneda = Monedas.query.filter_by(id=cuentanuevacredito['id_Moneda']).first()
			if moneda.id == 67:
				if int(creditoform.limite.data) < int(cuentanuevacredito['Saldo_COP']):
					return json.dumps('no')
				else:
					session['creditonuevo']={'Fecha_Pago':str(creditoform.fecha_pago.data), 'Limite_COP':str(int(creditoform.limite.data))}
					return json.dumps('si')
			else:
				if float(creditoform.limite.data) < float(cuentanuevacredito['Saldo']):
					return json.dumps('no')
				else:
					limite_cop= exchange.exchange(float(creditoform.limite.data), moneda.Simbolo, 'COP')
					limite_cop= round(limite_cop)
					session['creditonuevo']={'Fecha_Pago':str(creditoform.fecha_pago.data), 'Limite_COP':str(int(limite_cop)), 'Limite':str(float(creditoform.limite.data))}
					return json.dumps('si')
	return json.dumps(creditoform.errors)		

@app.route('/principal/cuentas/AddCuenta/CreditoAjaxDone')
@login_required
def CreditoAjaxDone():
	if 'cuentanuevacredito' in session:
		cuentanuevacredito=session['cuentanuevacredito']
		if 'creditonuevo' in session:
			creditonuevo=session['creditonuevo']
			moneda = Monedas.query.filter_by(id=cuentanuevacredito['id_Moneda']).first()
			if moneda.id == 67:
				cuentanueva= Cuentas(Saldo_COP=int(cuentanuevacredito['Saldo_COP']), Nombre=cuentanuevacredito['Nombre'], Logo=cuentanuevacredito['Logo'], Descripcion=cuentanuevacredito['Descripcion'], id_Usuario=cuentanuevacredito['id_Usuario'], id_Tipocuenta='2', id_Moneda=cuentanuevacredito['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				credito = Creditos(Fecha_Pago=creditonuevo['Fecha_Pago'], Limite_COP=int(creditonuevo['Limite_COP']), id_Cuenta=cuentanueva.id)
				db.session.add(credito)
				db.session.commit()
				session.pop('creditonuevo', None)
				session.pop('cuentanuevacredito', None)
				return redirect(url_for('cuentas'))
			else:
				cuentanueva= Cuentas(Saldo=float(cuentanuevacredito['Saldo']), Saldo_COP=int(cuentanuevacredito['Saldo_COP']), Nombre=cuentanuevacredito['Nombre'], Logo=cuentanuevacredito['Logo'], Descripcion=cuentanuevacredito['Descripcion'], id_Usuario=cuentanuevacredito['id_Usuario'], id_Tipocuenta='2', id_Moneda=cuentanuevacredito['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				credito = Creditos(Fecha_Pago=creditonuevo['Fecha_Pago'], Limite=float(creditonuevo['Limite']), Limite_COP=int(creditonuevo['Limite_COP']), id_Cuenta=cuentanueva.id)
				db.session.add(credito)
				db.session.commit()
				session.pop('creditonuevo', None)
				session.pop('cuentanuevacredito', None)
				return redirect(url_for('cuentas'))
		else:
			return redirect(url_for('AddCuenta'))
	else:
		return redirect(url_for('AddCuenta'))	

@app.route('/principal/cuentas/AddCuenta/PrestamoAjaxProcess', methods=['GET', 'POST'])
@login_required
def PrestamoAjaxProcess():
	if request.method == 'GET':
		return redirect(url_for('AddCuenta'))
	prestamoform = PrestamoForm(prefix='c')
	if prestamoform.validate_on_submit():
		if 'cuentanuevaprestamo' in session:
			cuentanuevaprestamo=session['cuentanuevaprestamo']
			moneda = Monedas.query.filter_by(id=cuentanuevaprestamo['id_Moneda']).first()
			if moneda.id == 67:
				session['prestamonuevo']={'Valor_Prestamo_COP':str(int(prestamoform.valor.data)), 'TAE':str(float(prestamoform.TAE.data)), 'Cuotas':str(int(prestamoform.cuotas.data)), 'Fecha_Pago':str(prestamoform.fecha_pago.data)}
				return json.dumps('si')
			else:
				valor_prestamo_cop= round(exchange.exchange(float(prestamoform.valor.data), moneda.Simbolo, 'COP'))
				session['prestamonuevo']={'Valor_Prestamo':str(float(prestamoform.valor.data)), 'Valor_Prestamo_COP':int(valor_prestamo_cop), 'TAE':str(float(prestamoform.TAE.data)), 'Cuotas':str(int(prestamoform.cuotas.data)), 'Fecha_Pago':str(prestamoform.fecha_pago.data)}
				return json.dumps('si')
	return json.dumps(prestamoform.errors)

	
@app.route('/principal/cuentas/AddCuenta/PrestamoAjaxDone')
@login_required
def PrestamoAjaxDone():
	if 'cuentanuevaprestamo' in session:
		cuentanuevaprestamo=session['cuentanuevaprestamo']
		if 'prestamonuevo' in session:
			prestamonuevo=session['prestamonuevo']
			moneda = Monedas.query.filter_by(id=cuentanuevaprestamo['id_Moneda']).first()
			if moneda.id == 67:
				cuentanueva= Cuentas(Saldo_COP=int(cuentanuevaprestamo['Saldo_COP']), Nombre=cuentanuevaprestamo['Nombre'], Logo=cuentanuevaprestamo['Logo'], Descripcion=cuentanuevaprestamo['Descripcion'], id_Usuario=cuentanuevaprestamo['id_Usuario'], id_Tipocuenta='4', id_Moneda=cuentanuevaprestamo['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				cuentaprestamo= Prestamos(TAE=prestamonuevo['TAE'], Cuotas=prestamonuevo['Cuotas'], Valor_Prestamo_COP=prestamonuevo['Valor_Prestamo_COP'], id_Cuenta=cuentanueva.id)
				db.session.add(cuentaprestamo)
				db.session.commit()
				#Plan de Pago
				calculo= round((((cuentaprestamo.TAE/100) * cuentaprestamo.Valor_Prestamo_COP)/(1 - ((1 + (cuentaprestamo.TAE/100))**-cuentaprestamo.Cuotas))))
				Fecha_Pago=datetime.datetime.strptime(prestamonuevo['Fecha_Pago'], '%Y-%m-%d').strftime('%m/%d/%y')
				plan_pago= Pago_prestamo(Dia_Pago=Fecha_Pago, Pago_Completo=False, Valor_Pagar_COP=int(calculo), id_Prestamo=cuentaprestamo.id)
				db.session.add(plan_pago)
				db.session.commit()
				session.pop('prestamonuevo', None)
				session.pop('cuentanuevaprestamo', None)
				return redirect(url_for('cuentas'))
			else:
				cuentanueva= Cuentas(Saldo=float(cuentanuevaprestamo['Saldo']), Saldo_COP=int(cuentanuevaprestamo['Saldo_COP']), Nombre=cuentanuevaprestamo['Nombre'], Logo=cuentanuevaprestamo['Logo'], Descripcion=cuentanuevaprestamo['Descripcion'], id_Usuario=cuentanuevaprestamo['id_Usuario'], id_Tipocuenta='4', id_Moneda=cuentanuevaprestamo['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				cuentaprestamo= Prestamos(TAE=prestamonuevo['TAE'], Cuotas=prestamonuevo['Cuotas'], Valor_Prestamo=prestamonuevo['Valor_Prestamo'], Valor_Prestamo_COP=prestamonuevo['Valor_Prestamo_COP'], id_Cuenta=cuentanueva.id)
				db.session.add(cuentaprestamo)
				db.session.commit()
				#Plan de Pago
				calculo= round((((cuentaprestamo.TAE/100) * cuentaprestamo.Valor_Prestamo)/(1 - ((1 + (cuentaprestamo.TAE/100))**-cuentaprestamo.Cuotas))))
				calculo_cop= round(exchange.exchange(float(calculo), moneda.Simbolo, 'COP'))
				Fecha_Pago=datetime.datetime.strptime(prestamonuevo['Fecha_Pago'], '%Y-%m-%d').strftime('%m/%d/%y')
				plan_pago= Pago_prestamo(Dia_Pago=Fecha_Pago, Pago_Completo=False, Valor_Pagar=calculo, Valor_Pagar_COP=int(calculo_cop), id_Prestamo=cuentaprestamo.id)
				db.session.add(plan_pago)
				db.session.commit()
				session.pop('prestamonuevo', None)
				session.pop('cuentanuevaprestamo', None)
				return redirect(url_for('cuentas'))
		else:
			return redirect(url_for('AddCuenta'))
	else:
		return redirect(url_for('AddCuenta'))



	
@app.route('/principal/cuentas/InfoCuentaCheque/Cheques')
@login_required
def chequesruta():
	id_cuenta = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id_cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
	return render_template('cheques.html', cuenta=cuenta, moneda=moneda, cheques=cheques)	
		
@app.route('/principal/cuentas/InfoCheque/Cheques/AddCheque', methods=['GET','POST'])
@login_required
def AddCheque():
	id_cuenta = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id_cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	form=ChequeForm()
	#Añadir Egreso
	return render_template('chequenuevo.html', form=form, cuenta=cuenta, moneda=moneda)

@app.route('/principal/cuentas/InfoCheque/Cheques/ChequeAjaxProcess', methods=['GET','POST'])
@login_required
def ChequeAjaxProcess():
	cuentaid = request.form.get("cuentaid",None)
	cuenta = Cuentas.query.filter_by(id=cuentaid).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	if request.method == 'GET':
		return redirect(url_for('AddCheque', id=cuentaid))
	form = ChequeForm()
	if form.validate_on_submit():
		if moneda.id == 67:
			if int(form.valor.data) > int(cuenta.Saldo_COP):
				return json.dumps('no')
			else:
				session['nuevocheque']={'Valor_COP':str(int(form.valor.data)), 'Fecha':form.fecha.data, 'id_Cuenta':cuenta.id }
				return json.dumps('si')
		else:
			if float(form.valor.data) > float(cuenta.Saldo):
				return json.dumps('no')
			else:
				valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
				valor_cop= round(valor_cop)
				session['nuevocheque']={'Valor':str(float(form.valor.data)), 'Valor_COP':str(int(valor_cop)), 'Fecha':form.fecha.data, 'id_Cuenta':cuenta.id }
				return json.dumps('si')
	return json.dumps(form.errors)	

@app.route('/principal/cuentas/InfoCheque/Cheques/ChequeAjaxDone')
@login_required
def ChequeAjaxDone():
	if 'nuevocheque' in session:
		nuevocheque=session['nuevocheque']
		cuenta = Cuentas.query.filter_by(id=nuevocheque['id_Cuenta']).first()
		moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
		if moneda.id == 67:
			cheque= Cheques(Valor_COP=int(nuevocheque['Valor_COP']), Fecha=nuevocheque['Fecha'], id_Cuenta=nuevocheque['id_Cuenta'])
			db.session.add(cheque)
			db.session.commit()
			transaccion= Transacciones(Fecha=cheque.Fecha, Valor_COP=cheque.Valor_COP, Tipo='Egreso', Descripcion='Egreso por cheque', id_Cuenta=cheque.id_Cuenta)
			db.session.add(transaccion)
			db.session.commit()
			cuenta.Saldo_COP=(cuenta.Saldo_COP - transaccion.Valor_COP)
			db.session.commit()
			session.pop('nuevocheque', None)
			flash('Egreso añadido en transacciones.'.decode('utf-8'))
			return redirect(url_for('chequesruta', id=cuenta.id))
		else:
			cheque= Cheques(Valor=float(nuevocheque['Valor']), Valor_COP=int(nuevocheque['Valor_COP']),Fecha=nuevocheque['Fecha'], id_Cuenta=nuevocheque['id_Cuenta'])
			db.session.add(cheque)
			db.session.commit()
			transaccion= Transacciones(Fecha=cheque.Fecha, Valor=cheque.Valor, Valor_COP=cheque.Valor_COP, Tipo='Egreso', Descripcion='Egreso por cheque', id_Cuenta=cheque.id_Cuenta)
			db.session.add(transaccion)
			db.session.commit()
			cuenta.Saldo=(cuenta.Saldo - transaccion.Valor)
			cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
			db.session.commit()
			session.pop('nuevocheque', None)
			flash('Egreso añadido en transacciones.'.decode('utf-8'))
			return redirect(url_for('chequesruta', id=cuenta.id))
	
@app.route('/principal/cuentas/InfoCheque/Cheques/DeleteCheque')
@login_required
def DeleteCheque():
	id_cheque = request.args.get('id', None)
	id_cuenta = request.args.get('id_cuenta', None)
	cheque = Cheques.query.filter_by(id=id_cheque).first()
	cuenta = Cuentas.query.filter_by(id=id_cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	if cuenta.id_Moneda == 67:
		transaccion= Transacciones(Fecha=cheque.Fecha, Valor_COP=cheque.Valor_COP, Tipo='Reembolso', Descripcion='Reembolso por cheque', id_Cuenta=cheque.id_Cuenta)
		db.session.add(transaccion)
		db.session.commit()
		cuenta.Saldo_COP=(cuenta.Saldo_COP + cheque.Valor_COP)
		db.session.commit()
		db.session.delete(cheque)
		db.session.commit()
		flash('Reembolso añadido en transacciones.'.decode('utf-8'))
		return redirect(url_for('chequesruta', id=cuenta.id))
	else:
		transaccion= Transacciones(Fecha=cheque.Fecha, Valor=cheque.Valor, Valor_COP=cheque.Valor_COP, Tipo='Reembolso', Descripcion='Reembolso por cheque', id_Cuenta=cheque.id_Cuenta)
		db.session.add(transaccion)
		db.session.commit()
		cuenta.Saldo=(cuenta.Saldo + cheque.Valor)
		cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
		db.session.commit()
		db.session.delete(cheque)
		db.session.commit()
		flash('Reembolso añadido en transacciones.'.decode('utf-8'))
		return redirect(url_for('chequesruta', id=cuenta.id))

@app.route('/principal/cuentas/InfoEfectivo')
@login_required
def infoefectivo():
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	return render_template('efectivoinfo.html', cuenta=cuenta, moneda=moneda)

@app.route('/principal/cuentas/InfoCredito')
@login_required
def infocredito():
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	return render_template('creditoinfo.html', cuenta=cuenta, moneda=moneda, credito=credito)
	
@app.route('/principal/cuentas/InfoCuentaCheque')
@login_required
def infocheque():
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	return render_template('chequeinfo.html', cuenta=cuenta, moneda=moneda)
	
@app.route('/principal/cuentas/InfoPrestamo')
@login_required
def infoprestamo():
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
	pago_prestamo= Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	return render_template('prestamoinfo.html', cuenta=cuenta, moneda=moneda, prestamo=prestamo, pago_prestamo=pago_prestamo)
	
@app.route('/principal/cuentas/DeleteAccount')
@login_required
def DeleteAccount():
	#Eliminar Transacciones
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	if cuenta.id_Tipocuenta == 1:
		#Efectivo
		transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
		for transaccion in transacciones:
			if transaccion is not None:
				transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
				for transferencia in transferencias:
					if transferencia is not None:
						db.session.delete(transferencia)
						db.session.commit()
				db.session.delete(transaccion)
				db.session.commit()
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 2:
		#Credito
		transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
		for transaccion in transacciones:
			if transaccion is not None:
				transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
				for transferencia in transferencias:
					if transferencia is not None:
						db.session.delete(transferencia)
						db.session.commit()
				db.session.delete(transaccion)
				db.session.commit()
		credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
		db.session.delete(credito)
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 3:
		#Cheque
		transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
		for transaccion in transacciones:
			if transaccion is not None:
				transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
				for transferencia in transferencias:
					if transferencia is not None:
						db.session.delete(transferencia)
						db.session.commit()
				db.session.delete(transaccion)
				db.session.commit()
		cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
		for cheque in cheques:
			if cheque is not None:
				db.session.delete(cheque)
				db.session.commit()
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 4:
		#Prestamo
		transacciones = Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
		for transaccion in transacciones:
			if transaccion is not None:
				transferencias = Transferencias.query.filter_by(id_Transaccion=transaccion.id).all()
				for transferencia in transferencias:
					if transferencia is not None:
						db.session.delete(transferencia)
						db.session.commit()
				db.session.delete(transaccion)
				db.session.commit()
		prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
		pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
		db.session.delete(pago_prestamo)
		db.session.delete(prestamo)
		db.session.delete(cuenta)
		db.session.commit()
	return redirect(url_for('cuentas'))

@app.route('/principal/transacciones')
@login_required
def transacciones():
	cuentas= Cuentas.query.all()
	if len(cuentas) == 0:
		flash('Añada cuentas para poder agregar transacciones.'.decode('utf-8'))
	monedas= Monedas.query.all()
	transacciones= Transacciones.query.all()
	transferencias= Transferencias.query.all()
	return render_template('transacciones.html', cuentas=cuentas, transacciones=transacciones, monedas=monedas, transferencias=transferencias)
	
@app.route('/principal/transacciones/AddTransaccion', methods=['GET', 'POST'])
@login_required
def AddTransaccion():
	cuentas= Cuentas.query.all()
	monedas= Monedas.query.all()
	if len(cuentas) == 0:
		flash('Añada cuentas para poder agregar transacciones.'.decode('utf-8'))
		return redirect(url_for('cuentas'))
	else:
		form=TransaccionForm()
		if form.validate_on_submit():
			cuentaform = request.form.get("oculto", None)
			cuenta= Cuentas.query.filter_by(id=cuentaform).first()
			moneda= Monedas.query.filter_by(id=cuenta.id_Moneda).first()
			#Peso Colombiano
			if cuenta.id_Moneda == 67:
				if form.tipo.data == '1':
					cuenta.Saldo_COP=(cuenta.Saldo_COP + int(form.valor.data))
					db.session.commit()
					transaccion= Transacciones(Fecha=form.fecha.data, Valor_COP=int(form.valor.data), Tipo='Ingreso', Descripcion=form.descripcion.data, id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					return redirect(url_for('transacciones'))
				elif form.tipo.data == '2':
					if int(form.valor.data) > cuenta.Saldo_COP:
						flash('Valor egreso mayor al saldo.')
						return redirect(url_for('AddTransaccion'))
					else:
						cuenta.Saldo_COP=(cuenta.Saldo_COP - int(form.valor.data))
						db.session.commit()
						transaccion= Transacciones(Fecha=form.fecha.data, Valor_COP=int(form.valor.data), Tipo='Egreso', Descripcion=form.descripcion.data, id_Cuenta=cuenta.id)
						db.session.add(transaccion)
						db.session.commit()
						return redirect(url_for('transacciones'))
				elif form.tipo.data == '3':
					if len(cuentas) == 1:
						flash('No es posible realizar transferencia.')
						return redirect(url_for('AddTransaccion'))
					else:
						if int(form.valor.data) > cuenta.Saldo_COP:
							flash('Valor transferencia mayor a saldo.')
							return redirect(url_for('AddTransaccion'))
						else:
							transferencianueva={'Fecha':form.fecha.data, 'Valor_COP':str(int(form.valor.data)), 'Tipo':'Transferencia', 'Descripcion':form.descripcion.data, 'id_Cuenta':cuenta.id}
							session['transferencianueva']=transferencianueva
							return redirect(url_for('transferencia'))
			else:
				if form.tipo.data == '1':
					valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
					valor_cop= round(valor_cop)
					cuenta.Saldo=(cuenta.Saldo + float(form.valor.data))
					db.session.commit()
					cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
					db.session.commit()
					transaccion= Transacciones(Fecha=form.fecha.data, Valor=form.valor.data, Valor_COP=int(valor_cop), Tipo='Ingreso', Descripcion=form.descripcion.data, id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					return redirect(url_for('transacciones'))
				elif form.tipo.data == '2':
					if form.valor.data > cuenta.Saldo:
						flash('Valor egreso mayor al saldo.')
						return redirect(url_for('AddTransaccion'))
					else:
						valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
						valor_cop= round(valor_cop)
						cuenta.Saldo=(cuenta.Saldo - float(form.valor.data))
						db.session.commit()
						cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
						db.session.commit()
						transaccion= Transacciones(Fecha=form.fecha.data, Valor=form.valor.data, Valor_COP=int(valor_cop), Tipo='Egreso', Descripcion=form.descripcion.data, id_Cuenta=cuenta.id)
						db.session.add(transaccion)
						db.session.commit()
						return redirect(url_for('transacciones')) 
				elif form.tipo.data == '3':
					if len(cuentas) == 1:
						flash('No es posible realizar transferencia.')
						return redirect(url_for('AddTransaccion'))
					else:
						if form.valor.data > cuenta.Saldo:
							flash('Valor transferencia mayor a saldo.')
							return redirect(url_for('AddTransaccion'))
						else:
							valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
							valor_cop= round(valor_cop)
							transferencianueva={'Fecha':form.fecha.data, 'Valor':str(form.valor.data), 'Valor_COP':str(int(valor_cop)), 'Tipo':'Transferencia', 'Descripcion':form.descripcion.data, 'id_Cuenta':cuenta.id}
							session['transferencianueva']=transferencianueva
							return redirect(url_for('transferencia'))
	return render_template('nuevatransaccion.html', form=form, cuentas=cuentas, monedas=monedas)
	
@app.route('/principal/transacciones/AddTransaccion/Transferencia', methods=['GET', 'POST'])
@login_required
def transferencia():
	if 'transferencianueva' in session:
		monedas = Monedas.query.all()
		cuentas = Cuentas.query.all()
		tipocuentas = Tipocuenta.query.all()
		transferencianueva=session['transferencianueva']
		cuenta = Cuentas.query.filter_by(id=transferencianueva['id_Cuenta']).first()
		moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
		form=TransferenciaForm()
		if form.validate_on_submit():
			if cuenta.id_Moneda == 67:
				cuenta.Saldo_COP=(cuenta.Saldo_COP - int(transferencianueva['Valor_COP']))
				db.session.commit()
				cuentaform = request.form.get("oculto", None)
				cuenta_destino = Cuentas.query.filter_by(id=cuentaform).first()
				moneda_destino = Monedas.query.filter_by(id=cuenta_destino.id_Moneda).first()
				if cuenta_destino.id_Moneda == 67:
					cuenta_destino.Saldo_COP=(cuenta_destino.Saldo_COP + int(transferencianueva['Valor_COP']))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id, id_MonedaDestino=moneda_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
				else:
					valor= exchange.exchange(int(transferencianueva['Valor_COP']), 'COP', moneda_destino.Simbolo)
					valor= round(valor, 2)
					cuenta_destino.Saldo=(cuenta_destino.Saldo + float(valor))
					db.session.commit()
					cuenta_destino.Saldo_COP=int(round(exchange.exchange(float(cuenta_destino.Saldo), moneda_destino.Simbolo, 'COP')))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, Valor=float(valor), id_CuentaDestino=cuenta_destino.id, id_MonedaDestino=moneda_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
			else:
				cuenta.Saldo=(cuenta.Saldo - float(transferencianueva['Valor']))
				db.session.commit()
				cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
				db.session.commit()
				cuentaform = request.form.get("oculto", None)
				cuenta_destino = Cuentas.query.filter_by(id=cuentaform).first()
				moneda_destino = Monedas.query.filter_by(id=cuenta_destino.id_Moneda).first()
				if cuenta_destino.id_Moneda == 67:
					cuenta_destino.Saldo_COP=(cuenta_destino.Saldo_COP + int(transferencianueva['Valor_COP']))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor=transferencianueva['Valor'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id, id_MonedaDestino=moneda_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
				else:
					if cuenta.id_Moneda == cuenta_destino.id_Moneda:
						valor=transferencianueva['Valor']
					else:
						valor= exchange.exchange(float(transferencianueva['Valor']), moneda.Simbolo, moneda_destino.Simbolo)
						valor= round(valor, 2)
					cuenta_destino.Saldo=(cuenta_destino.Saldo + float(valor))
					db.session.commit()
					cuenta_destino.Saldo_COP=int(round(exchange.exchange(float(cuenta_destino.Saldo), moneda_destino.Simbolo, 'COP')))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor=transferencianueva['Valor'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					if cuenta.id_Moneda == cuenta_destino.id_Moneda:
						transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id, id_MonedaDestino=moneda_destino.id)
						db.session.add(transferenciabase)
						db.session.commit()
						return redirect(url_for('transacciones'))
					else:
						transferenciabase= Transferencias(id_Transaccion=transaccion.id, Valor=float(valor), id_CuentaDestino=cuenta_destino.id, id_MonedaDestino=moneda_destino.id)
						db.session.add(transferenciabase)
						db.session.commit()
						return redirect(url_for('transacciones'))
	else:
		return redirect(url_for('transacciones'))
	return render_template('transferencianueva.html', form=form, cuentas=cuentas, cuentaorigen=cuenta, transferencia=transferencianueva, moneda=moneda, tipocuentas=tipocuentas, monedas=monedas)
	
@app.route('/principal/transacciones/InfoIngreso')
@login_required
def infoingreso():
	id = request.args.get('id', None)
	transaccion = Transacciones.query.filter_by(id=id).first()
	cuenta = Cuentas.query.filter_by(id=transaccion.id_Cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	tipocuentas = Tipocuenta.query.all()
	return render_template('IngresoInfo.html', moneda=moneda, cuentaorigen=cuenta, tipocuentas=tipocuentas, ingreso=transaccion)	
	
	
@app.route('/principal/transacciones/InfoEgreso')
@login_required
def infoegreso():
	id = request.args.get('id', None)
	transaccion = Transacciones.query.filter_by(id=id).first()
	cuenta = Cuentas.query.filter_by(id=transaccion.id_Cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	tipocuentas = Tipocuenta.query.all()
	return render_template('EgresoInfo.html', moneda=moneda, cuentaorigen=cuenta, tipocuentas=tipocuentas, Egreso=transaccion)

@app.route('/principal/transacciones/InfoReembolso')
@login_required
def inforeembolso():
	id = request.args.get('id', None)
	transaccion = Transacciones.query.filter_by(id=id).first()
	cuenta = Cuentas.query.filter_by(id=transaccion.id_Cuenta).first()
	if cuenta.id_Tipocuenta != 3:
		return redirect(url_for('transacciones'))
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	tipocuentas = Tipocuenta.query.all()
	return render_template('ReembolsoInfo.html', moneda=moneda, cuentaorigen=cuenta, tipocuentas=tipocuentas, Reembolso=transaccion)	

@app.route('/principal/transacciones/InfoTransferencia')
@login_required
def infotransferencia():
	id = request.args.get('id', None)
	transaccion = Transacciones.query.filter_by(id=id).first()
	transference = Transferencias.query.filter_by(id_Transaccion=transaccion.id).first()
	cuentadestino = Cuentas.query.filter_by(id=transference.id_CuentaDestino).first()
	cuenta = Cuentas.query.filter_by(id=transaccion.id_Cuenta).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	monedadestino = Monedas.query.filter_by(id=cuentadestino.id_Moneda).first()
	tipocuentas = Tipocuenta.query.all()
	return render_template('TransferenciaInfo.html', moneda=moneda, cuentaorigen=cuenta, monedadestino=monedadestino, cuentadestino=cuentadestino, tipocuentas=tipocuentas, transferencia=transaccion, transference=transference)	
	
@app.route('/principal/transacciones/transaccionescuenta')
@login_required
def transaccionescuenta():
	id = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id).first()
	moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
	transacciones= Transacciones.query.filter_by(id_Cuenta=cuenta.id).all()
	if not transacciones:
		flash('No hay transacciones asociadas a ésta cuenta.'.decode('utf-8'))
		return redirect(url_for('info', id=cuenta.id))
	transferencias= Transferencias.query.all()
	monedas= Monedas.query.all()
	return render_template('transaccionescuenta.html', moneda=moneda, monedas=monedas, cuenta=cuenta, transferencias=transferencias, transacciones=transacciones)	

@app.route('/info')
@login_required
def info():
	id = request.args.get('id', None)
	cuenta= Cuentas.query.filter_by(id=id).first()
	if cuenta.id_Tipocuenta == 1:
		return redirect(url_for('infoefectivo', id=cuenta.id))
	elif cuenta.id_Tipocuenta == 2:
		return redirect(url_for('infocredito', id=cuenta.id))
	elif cuenta.id_Tipocuenta == 3:
		return redirect(url_for('infocheque', id=cuenta.id))
	elif cuenta.id_Tipocuenta == 4:
		return redirect(url_for('infoprestamo', id=cuenta.id))

#Sumar ingresos, egresos,transferencias reembolsos, vista individual transacciones de cuenta, vista individual transaccion, vista individual transferencia = Ingreso y egreso
#Crear bien cheque y reembolso, cuenta destino borrada, añadir egreso con cheque