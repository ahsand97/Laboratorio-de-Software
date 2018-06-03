#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, session
from Proyecto import app, db #app es la variable de __init__.py que es parte de la carpeta Proyecto, db es la base de datos
from Proyecto.forms import LoginForm, RegistrationForm, CuentaForm, EditarNombre, EditarUsuario, EditarCorreo, EditarClave, CreditoForm, ChequeForm, PrestamoForm, TransaccionForm, TransferenciaForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from Proyecto.modelos import Usuarios, Cuentas, Tipocuenta, Monedas, Creditos, Cheques, Prestamos, Pago_prestamo, Transacciones, Reembolsos, Transferencias
from openexchangerates.exchange import Exchange #Moneda

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
	user = Usuarios.query.filter_by(Usuario='Estandar').first()
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
	if form.validate_on_submit():
		user = Usuarios.query.filter_by(Usuario=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Usuario o contraseña no válidos.'.decode('utf-8'))
			return redirect(url_for('login'))
		login_user(user)
		return redirect(url_for('principal'))																											
	return render_template('login.html', form=form, users=users)

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
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 2:
			credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
			db.session.delete(credito)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 3:
			cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
			for cheque in cheques:
				if cheque is not None:
					db.session.delete(cheque)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 4:
			prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
			pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
			if pago_prestamo is not None:
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
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 2:
			credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
			db.session.delete(credito)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 3:
			cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
			for cheque in cheques:
				if cheque is not None:
					db.session.delete(cheque)
			db.session.delete(cuenta)
			db.session.commit()
		elif cuenta.id_Tipocuenta == 4:
			prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
			pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
			if pago_prestamo is not None:
				db.session.delete(pago_prestamo)
			db.session.delete(prestamo)
			db.session.delete(cuenta)
			db.session.commit()
	flash('Sus cuentas han sido eliminadas.')
	return redirect(url_for('principal'))
	
@app.route('/EditProfile')
@login_required
def EditProfile():
	return render_template('editarperfil.html')
	
@app.route('/EditProfile/ChangeName', methods=['GET','POST'])
@login_required
def ChangesProfileName():
	form = EditarNombre()
	if form.validate_on_submit():
		usuario= Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Nombre= form.nombre.data
		db.session.commit()
		flash('Nombre cambiado.')
		return redirect(url_for('EditProfile'))
	return render_template('cambionombre.html', form=form)
	
@app.route('/EditProfile/ChangeUsername', methods=['GET','POST'])
@login_required
def ChangesProfileUsername():
	form = EditarUsuario()
	if form.validate_on_submit():
		usuario= Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Usuario= form.usuario.data
		db.session.commit()
		flash('Nombre de Usuario cambiado.')
		return redirect(url_for('EditProfile'))
	return render_template('cambiousuario.html', form=form)
	
@app.route('/EditProfile/ChangeEmail', methods=['GET','POST'])
@login_required
def ChangesProfileEmail():
	form = EditarCorreo()
	if form.validate_on_submit():
		usuario= Usuarios.query.filter_by(id=current_user.id).first()
		usuario.Correo= form.email.data
		db.session.commit()
		flash('Dirección de Correo Electrónico cambiada.'.decode('utf-8'))
		return redirect(url_for('EditProfile'))
	return render_template('cambioemail.html', form=form)

@app.route('/EditProfile/ChangePassword', methods=['GET','POST'])
@login_required
def ChangesProfilePassword():
	form = EditarClave()
	if form.validate_on_submit():
		usuario= Usuarios.query.filter_by(id=current_user.id).first()
		if usuario.check_password(form.passwordactual.data) == True:
			usuario.set_password(form.password.data)
			db.session.commit()
			flash('Contraseña cambiada.'.decode('utf-8'))
			return redirect(url_for('EditProfile'))
		else:
			flash('Contraseña Incorrecta.'.decode('utf-8'))
			return redirect(url_for('ChangesProfilePassword'))
	return render_template('cambioclave.html', form=form)	

@app.route('/registro', methods=['GET', 'POST'])
def registro():
	users = Usuarios.query.all()
	if current_user.is_authenticated:
		user=current_user
		if user.Usuario != 'Estandar':
			return redirect(url_for('principal'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = Usuarios(Nombre=form.name.data, Usuario=form.username.data, Correo=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Registro Exitoso.', 'registroexitoso')
		return redirect(url_for('login'))
	return render_template('registro.html', form=form, users=users)
		
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
	form=CuentaForm()
	if form.validate_on_submit():
		cuenta= Cuentas.query.filter_by(Nombre=form.nombre.data).first()
		moneda= Monedas.query.filter_by(Simbolo=form.moneda.data).first()
		if cuenta is not None:
			flash('Ya tienes una cuenta con ese nombre.')
			return redirect(url_for('AddCuenta'))
		else:
#-----------------Efectivo----------------------------------------------------------------------
			if form.categoria.data == '1':
				if moneda.id == 67:
					logoform = request.form.get("oculto", None)
					cuentanueva= Cuentas(Saldo_COP=int(form.saldo.data), Nombre=form.nombre.data, Logo=logoform, Descripcion=form.descripcion.data, id_Usuario=usuario.id, id_Tipocuenta='1', id_Moneda=moneda.id)
					db.session.add(cuentanueva)
					db.session.commit()
					return redirect(url_for('cuentas'))
				else:
					saldo_cop= exchange.exchange(float(form.saldo.data), moneda.Simbolo, 'COP')
					saldo_cop= round(saldo_cop)
					logoform = request.form.get("oculto", None)
					cuentanueva= Cuentas(Saldo=form.saldo.data, Saldo_COP=int(saldo_cop), Nombre=form.nombre.data, Logo=logoform, Descripcion=form.descripcion.data, id_Usuario=usuario.id, id_Tipocuenta='1', id_Moneda=moneda.id)
					db.session.add(cuentanueva)
					db.session.commit()
					return redirect(url_for('cuentas'))
#-----------------Crédito------------------------------------------------------------------------
			elif form.categoria.data == '2':
				if moneda.id == 67:
					logoform = request.form.get("oculto", None)
					cuentanueva= {'Saldo_COP':str(int(form.saldo.data)), 'Nombre':form.nombre.data, 'Logo':logoform, 'Descripcion':form.descripcion.data, 'id_Usuario':usuario.id, 'id_Tipocuenta':'2', 'id_Moneda':moneda.id}
					session['cuentanuevacredito']=cuentanueva
					return redirect(url_for('credito'))
				else:
					saldo_cop= exchange.exchange(float(form.saldo.data), moneda.Simbolo, 'COP')
					saldo_cop= round(saldo_cop)
					logoform = request.form.get("oculto", None)
					cuentanueva= {'Saldo':str(form.saldo.data), 'Saldo_COP':str(int(saldo_cop)), 'Nombre':form.nombre.data, 'Logo':logoform, 'Descripcion':form.descripcion.data, 'id_Usuario':usuario.id, 'id_Tipocuenta':'2', 'id_Moneda':moneda.id}
					session['cuentanuevacredito']=cuentanueva
					return redirect(url_for('credito'))
#-----------------Cheque--------------------------------------------------------------------------
			elif form.categoria.data == '3':
				if moneda.id == 67:
					logoform = request.form.get("oculto", None)
					cuentanueva= Cuentas(Saldo_COP=int(form.saldo.data), Nombre=form.nombre.data, Logo=logoform, Descripcion=form.descripcion.data, id_Usuario=usuario.id, id_Tipocuenta='3', id_Moneda=moneda.id)
					db.session.add(cuentanueva)
					db.session.commit()
					return redirect(url_for('cuentas'))
				else:
					saldo_cop= exchange.exchange(float(form.saldo.data), moneda.Simbolo, 'COP')
					saldo_cop= round(saldo_cop)
					logoform = request.form.get("oculto", None)
					cuentanueva= Cuentas(Saldo=form.saldo.data, Saldo_COP=int(saldo_cop), Nombre=form.nombre.data, Logo=logoform, Descripcion=form.descripcion.data, id_Usuario=usuario.id, id_Tipocuenta='3', id_Moneda=moneda.id)
					db.session.add(cuentanueva)
					db.session.commit()
					return redirect(url_for('cuentas'))
#------------------Préstamo-----------------------------------------------------------------------			
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
					return redirect(url_for('prestamo'))
	return render_template('nuevacuenta.html', form=form, usuario=usuario)

	
@app.route('/principal/cuentas/AddCuenta/credito', methods=['GET','POST'])
@login_required
def credito():
	if 'cuentanuevacredito' in session:
		cuentanuevacredito=session['cuentanuevacredito']
		moneda = Monedas.query.filter_by(id=cuentanuevacredito['id_Moneda']).first()
		form=CreditoForm()
		if form.validate_on_submit():
			if moneda.id == 67:
				cuentanueva= Cuentas(Saldo_COP=int(cuentanuevacredito['Saldo_COP']), Nombre=cuentanuevacredito['Nombre'], Logo=cuentanuevacredito['Logo'], Descripcion=cuentanuevacredito['Descripcion'], id_Usuario=cuentanuevacredito['id_Usuario'], id_Tipocuenta='2', id_Moneda=cuentanuevacredito['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				cuentacredito = Creditos(Fecha_Pago=form.fecha_pago.data, Limite_COP=int(form.limite.data), id_Cuenta=cuentanueva.id)
				db.session.add(cuentacredito)
				db.session.commit()
				return redirect(url_for('cuentas'))
			else:
				cuentanueva= Cuentas(Saldo=float(cuentanuevacredito['Saldo']), Saldo_COP=int(cuentanuevacredito['Saldo_COP']), Nombre=cuentanuevacredito['Nombre'], Logo=cuentanuevacredito['Logo'], Descripcion=cuentanuevacredito['Descripcion'], id_Usuario=cuentanuevacredito['id_Usuario'], id_Tipocuenta='2', id_Moneda=cuentanuevacredito['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				limite_cop= exchange.exchange(float(form.limite.data), moneda.Simbolo, 'COP')
				limite_cop= round(limite_cop)
				cuentacredito = Creditos(Fecha_Pago=form.fecha_pago.data, Limite=form.limite.data, Limite_COP=int(limite_cop), id_Cuenta=cuentanueva.id)
				db.session.add(cuentacredito)
				db.session.commit()
				return redirect(url_for('cuentas'))
	else:
		return redirect(url_for('cuentas'))
	return render_template('creditonuevo.html', form=form, cuenta=cuentanuevacredito, moneda=moneda)
	
'''@app.route('/principal/cuentas/AddCuenta/credito/nocredito')
@login_required
def nocredito():
	id_cuenta = request.args.get('id', None)
	cuenta = Cuentas.query.filter_by(id=id_cuenta).first()
	db.session.delete(cuenta)
	db.session.commit()
	return redirect(url_for('cuentas'))
'''

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
	if form.validate_on_submit():
		if moneda.id == 67:
			cheque = Cheques(Valor_COP=int(form.valor.data), Fecha=form.fecha.data, id_Cuenta=cuenta.id)
			db.session.add(cheque)
			db.session.commit()
			return redirect(url_for('chequesruta', id=cuenta.id))
		else:
			valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
			valor_cop= round(valor_cop)
			cheque = Cheques(Valor=form.valor.data, Valor_COP=int(valor_cop), Fecha=form.fecha.data, id_Cuenta=cuenta.id)
			db.session.add(cheque)
			db.session.commit()
			return redirect(url_for('chequesruta', id=cuenta.id))
	return render_template('chequenuevo.html', form=form, cuenta=cuenta, moneda=moneda)

@app.route('/principal/cuentas/InfoCheque/Cheques/DeleteCheque')
@login_required
def DeleteCheque():
	id_cheque = request.args.get('id', None)
	id_cuenta = request.args.get('id_cuenta', None)
	cheque = Cheques.query.filter_by(id=id_cheque).first()
	db.session.delete(cheque)
	db.session.commit()
	#Añadir Transacción
	return redirect(url_for('chequesruta', id=id_cuenta))

@app.route('/principal/cuentas/AddCuenta/prestamo', methods=['GET','POST'])
@login_required
def prestamo():
	if 'cuentanuevaprestamo' in session:
		cuentanuevaprestamo=session['cuentanuevaprestamo']
		moneda = Monedas.query.filter_by(id=cuentanuevaprestamo['id_Moneda']).first()
		form=PrestamoForm()
		if form.validate_on_submit():
			if moneda.id == 67:
				cuentanueva= Cuentas(Saldo_COP=int(cuentanuevaprestamo['Saldo_COP']), Nombre=cuentanuevaprestamo['Nombre'], Logo=cuentanuevaprestamo['Logo'], Descripcion=cuentanuevaprestamo['Descripcion'], id_Usuario=cuentanuevaprestamo['id_Usuario'], id_Tipocuenta='4', id_Moneda=cuentanuevaprestamo['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				cuentaprestamo = Prestamos(Valor_Prestamo_COP=int(form.valor.data), Cuotas=form.cuotas.data, id_Cuenta=cuentanueva.id, TAE=form.TAE.data)
				db.session.add(cuentaprestamo)
				db.session.commit()
				#Plan de Pago
				calculo= round((((cuentaprestamo.TAE/100) * cuentaprestamo.Valor_Prestamo_COP)/(1 - ((1 + (cuentaprestamo.TAE/100))**-cuentaprestamo.Cuotas))))
				plan_ago= Pago_prestamo(Dia_Pago=form.fecha_pago.data, Pago_Completo=False, Valor_Pagar_COP=int(calculo), id_Prestamo=cuentaprestamo.id)
				db.session.add(plan_ago)
				db.session.commit()
				return redirect(url_for('cuentas'))
			else:
				cuentanueva= Cuentas(Saldo=float(cuentanuevaprestamo['Saldo']), Saldo_COP=int(cuentanuevaprestamo['Saldo_COP']), Nombre=cuentanuevaprestamo['Nombre'], Logo=cuentanuevaprestamo['Logo'], Descripcion=cuentanuevaprestamo['Descripcion'], id_Usuario=cuentanuevaprestamo['id_Usuario'], id_Tipocuenta='4', id_Moneda=cuentanuevaprestamo['id_Moneda'])
				db.session.add(cuentanueva)
				db.session.commit()
				valor_prestamo_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
				valor_prestamo_cop= round(valor_prestamo_cop)
				cuentaprestamo = Prestamos(Valor_Prestamo=form.valor.data, Valor_Prestamo_COP=int(valor_prestamo_cop), Cuotas=form.cuotas.data, id_Cuenta=cuentanueva.id, TAE=form.TAE.data)
				db.session.add(cuentaprestamo)
				db.session.commit()
				#Añadir Plan de Pago
				calculo= round((((cuentaprestamo.TAE/100) * cuentaprestamo.Valor_Prestamo)/(1 - ((1 + (cuentaprestamo.TAE/100))**-cuentaprestamo.Cuotas))), 2)
				calculo_cop= exchange.exchange(calculo, moneda.Simbolo, 'COP')
				plan_ago= Pago_prestamo(Dia_Pago=form.fecha_pago.data, Pago_Completo=False, Valor_Pagar=calculo, Valor_Pagar_COP=int(calculo_cop), id_Prestamo=cuentaprestamo.id)
				db.session.add(plan_ago)
				db.session.commit()
				return redirect(url_for('cuentas'))
	else:
		return redirect(url_for('cuentas'))
	return render_template('prestamonuevo.html', form=form, cuenta=cuentanuevaprestamo, moneda=moneda)

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
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 2:
		credito = Creditos.query.filter_by(id_Cuenta=cuenta.id).first()
		db.session.delete(credito)
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 3:
		cheques = Cheques.query.filter_by(id_Cuenta=cuenta.id).all()
		for cheque in cheques:
			if cheque is not None:
				db.session.delete(cheque)
		db.session.delete(cuenta)
		db.session.commit()
	elif cuenta.id_Tipocuenta == 4:
		prestamo = Prestamos.query.filter_by(id_Cuenta=cuenta.id).first()
		pago_prestamo = Pago_prestamo.query.filter_by(id_Prestamo=prestamo.id).first()
		if pago_prestamo is not None:
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
	reembolsos = Reembolsos.query.all()
	transferencias= Transferencias.query.all()
	return render_template('transacciones.html', cuentas=cuentas, transacciones=transacciones, monedas=monedas, reembolsos=reembolsos, transferencias=transferencias)
	
@app.route('/principal/transacciones/AddTransaccion', methods=['GET', 'POST'])
@login_required
def AddTransaccion():
	cuentas= Cuentas.query.all()
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
					if form.valor.data > cuenta.Saldo:
						flash('Valor transferencia mayor a saldo.')
						return redirect(url_for('AddTransaccion'))
					else:
						valor_cop= exchange.exchange(float(form.valor.data), moneda.Simbolo, 'COP')
						valor_cop= round(valor_cop)
						transferencianueva={'Fecha':form.fecha.data, 'Valor':str(form.valor.data), 'Valor_COP':str(int(valor_cop)), 'Tipo':'Transferencia', 'Descripcion':form.descripcion.data, 'id_Cuenta':cuenta.id}
						session['transferencianueva']=transferencianueva
						return redirect(url_for('transferencia'))
	return render_template('nuevatransaccion.html', form=form, cuentas=cuentas)
	
@app.route('/principal/transacciones/AddTransaccion/Transferencia', methods=['GET', 'POST'])
@login_required
def transferencia():
	if 'transferencianueva' in session:
		cuentas = Cuentas.query.all()
		transferencianueva=session['transferencianueva']
		cuenta = Cuentas.query.filter_by(id=transferencianueva['id_Cuenta']).first()
		moneda = Monedas.query.filter_by(id=cuenta.id_Moneda).first()
		form=TransferenciaForm()
		if form.validate_on_submit():
			if cuenta.id_Moneda == 67:
				cuenta.Saldo_COP=(cuenta.Saldo_COP - int(transferencianueva['Valor_COP']))
				db.session.commit()
				cuenta_destino = Cuentas.query.filter_by(id=form.Cuenta_Destino).first()
				moneda_destino = Monedas.query.filter_by(id=cuenta_destino.id_Moneda).first()
				if cuenta_destino.id_Moneda == 67:
					cuenta_destino.Saldo_COP=(cuenta_destino.Saldo_COP + int(transferencianueva['Valor_COP']))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id)
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
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
			else:
				cuenta.Saldo=(cuenta.Saldo - float(transferencianueva['Valor']))
				db.session.commit()
				cuenta.Saldo_COP=int(round(exchange.exchange(float(cuenta.Saldo), moneda.Simbolo, 'COP')))
				db.session.commit()
				cuenta_destino = Cuentas.query.filter_by(id=form.Cuenta_Destino).first()
				moneda_destino = Monedas.query.filter_by(id=cuenta_destino.id_Moneda).first()
				if cuenta_destino.id_Moneda == 67:
					cuenta_destino.Saldo_COP=(cuenta_destino.Saldo_COP + int(transferencianueva['Valor_COP']))
					db.session.commit()
					transaccion= Transacciones(Fecha=transferencianueva['Fecha'], Valor=transferencianueva['Valor'], Valor_COP=transferencianueva['Valor_COP'], Tipo='Transferencia', Descripcion=transferencianueva['Descripcion'], id_Cuenta=cuenta.id)
					db.session.add(transaccion)
					db.session.commit()
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
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
					transferenciabase= Transferencias(id_Transaccion=transaccion.id, id_CuentaDestino=cuenta_destino.id)
					db.session.add(transferenciabase)
					db.session.commit()
					return redirect(url_for('transacciones'))
	else:
		return redirect(url_for('transacciones'))
	return render_template('transferencianueva.html', form=form, cuentas=cuentas, cuentaorigen=cuenta, transferencia=transferencianueva, moneda=moneda)
#Sumar ingresos, egresos, borrar bien todo, transferencias, reembolsos, vista individual transacciones de cuenta, vista individual transaccion, vista individual transferencia = Ingreso y egreso