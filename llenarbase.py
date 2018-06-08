from Proyecto import db
from Proyecto.modelos import Tipocuenta, Monedas, Usuarios
###################################################################
user = Usuarios(Nombre='Estandar', Usuario='a', Correo='a')
user.set_password('123')
db.session.add(user)
###################################################################
a = Tipocuenta(Nombre='Efectivo')
db.session.add(a)

b = Tipocuenta(Nombre='Credito')
db.session.add(b)

c = Tipocuenta(Nombre='Cheque')
db.session.add(c)

d = Tipocuenta(Nombre='Prestamo')
db.session.add(d)
####################################################################
ab = Monedas(Nombre="Afgani Afgano", Simbolo="AFN")
db.session.add(ab)

ac = Monedas(Nombre="Balboa", Simbolo="PAB")
db.session.add(ac)

ad = Monedas(Nombre="Bitcoin", Simbolo="BTC")
db.session.add(ad)

ae = Monedas(Nombre="Bolivar Fuerte", Simbolo="VEF")
db.session.add(ae)

af = Monedas(Nombre="Boliviano", Simbolo="BOB")
db.session.add(af)

ag = Monedas(Nombre="Chelin Keniano", Simbolo="KES")
db.session.add(ag)

ah = Monedas(Nombre="Colon Costarricense", Simbolo="CRC")
db.session.add(ah)

ai = Monedas(Nombre="Colon del Salvador", Simbolo="SVC")
db.session.add(ai)

aj = Monedas(Nombre="Corona Checa", Simbolo="CZK")
db.session.add(aj)

ak = Monedas(Nombre="Corona Danesa", Simbolo="DKK")
db.session.add(ak)

al = Monedas(Nombre="Corona Islandesa", Simbolo="ISK")
db.session.add(al)

am = Monedas(Nombre="Corona Sueca", Simbolo="SEK")
db.session.add(am)

an = Monedas(Nombre="Denar Macedonio", Simbolo="MKD")
db.session.add(an)

ao = Monedas(Nombre="Dinar Algerino", Simbolo="DZD")
db.session.add(ao)

ap = Monedas(Nombre="Dinar Tuniso", Simbolo="TND")
db.session.add(ap)

aq = Monedas(Nombre="Dinar Iraqui", Simbolo="IQD")
db.session.add(aq)

ar = Monedas(Nombre="Dinar Jordano", Simbolo="JOD")
db.session.add(ar)

ass = Monedas(Nombre="Dinar Libio", Simbolo="LYD")
db.session.add(ass)

at = Monedas(Nombre="Dinar Serbio", Simbolo="RSD")
db.session.add(at)

au = Monedas(Nombre="Dirham Marroqui", Simbolo="MAD")
db.session.add(au)

avc = Monedas(Nombre="Dirham de los Emiratos Arabes Unidos", Simbolo="AED")
db.session.add(avc)

awb = Monedas(Nombre="Dolar Australiano", Simbolo="AUD")
db.session.add(awb)

afc = Monedas(Nombre="Dolar Canadiense", Simbolo="CAD")
db.session.add(afc)

asb = Monedas(Nombre="Dolar Estadounidense", Simbolo="USD")
db.session.add(asb)

acx = Monedas(Nombre="Dolar Guyanes", Simbolo="GYD")
db.session.add(acx)

aby = Monedas(Nombre="Dolar Jamaiquino", Simbolo="JMD")
db.session.add(aby)

acz = Monedas(Nombre="Dolar Liberiano", Simbolo="LRD")
db.session.add(acz)

ba = Monedas(Nombre="Dolar Surinames", Simbolo="SRD")
db.session.add(ba)

bb = Monedas(Nombre="Dolar de Barbados", Simbolo="BBD")
db.session.add(bb)

bc = Monedas(Nombre="Dolar de Hong Kong", Simbolo="HKD")
db.session.add(bc)

bd = Monedas(Nombre="Dolar de Nueva Zelanda", Simbolo="NZD")
db.session.add(bd)

be = Monedas(Nombre="Dolar de Singapore", Simbolo="SGD")
db.session.add(be)

bf = Monedas(Nombre="Dolar de Trinidad y Tobago", Simbolo="TTD")
db.session.add(bf)

bh = Monedas(Nombre="Dolar de las Islas Caiman", Simbolo="KYD")
db.session.add(bh)

bi = Monedas(Nombre="Dram Armenio", Simbolo="AMD")
db.session.add(bi)

bj = Monedas(Nombre="Euro", Simbolo="EUR")
db.session.add(bj)

bk = Monedas(Nombre="Florin Antillanoneerlandes", Simbolo="ANG")
db.session.add(bk)

bl = Monedas(Nombre="Florin de Aruba", Simbolo="AWG")
db.session.add(bl)

bm = Monedas(Nombre="Forinto Hungaro", Simbolo="HUF")
db.session.add(bm)

bn = Monedas(Nombre="Franco Suizo", Simbolo="CHF")
db.session.add(bn)

bo = Monedas(Nombre="Gourde Haitiano", Simbolo="HTG")
db.session.add(bo)

bp = Monedas(Nombre="Grivna Ucraniana", Simbolo="UAH")
db.session.add(bp)

bq = Monedas(Nombre="Guarani", Simbolo="PYG")
db.session.add(bq)

br = Monedas(Nombre="Kip Laosiano", Simbolo="LAK")
db.session.add(br)

bs = Monedas(Nombre="Krone Noruego", Simbolo="NOK")
db.session.add(bs)

bt = Monedas(Nombre="Kuna croata", Simbolo="HRK")
db.session.add(bt)

bu = Monedas(Nombre="Kwanza de Angola", Simbolo="AOA")
db.session.add(bu)

bw = Monedas(Nombre="Lek Albanes", Simbolo="ALL")
db.session.add(bw)

bx = Monedas(Nombre="Lempira de Honduras", Simbolo="HNL")
db.session.add(bx)

by = Monedas(Nombre="Leu Moldavo", Simbolo="MDL")
db.session.add(by)

bz = Monedas(Nombre="Leu Rumano", Simbolo="RON")
db.session.add(bz)

ca = Monedas(Nombre="Lev Bulgaro", Simbolo="BGN")
db.session.add(ca)

cb = Monedas(Nombre="Libra Egipcia", Simbolo="EGP")
db.session.add(cb)

cc = Monedas(Nombre="Libra Esterlina", Simbolo="AED")
db.session.add(cc)

cd = Monedas(Nombre="Libra Libanesa", Simbolo="LBP")
db.session.add(cd)

ce = Monedas(Nombre="Libra Siria", Simbolo="SYP")
db.session.add(ce)

cf = Monedas(Nombre="Libra Sudanesa", Simbolo="SDG")
db.session.add(cf)

cg = Monedas(Nombre="Lira Turca", Simbolo="TRY")
db.session.add(cg)

ch = Monedas(Nombre="Manat Azerbaiyano", Simbolo="AZN")
db.session.add(ch)

ci = Monedas(Nombre="Marco Bosnioherzegovino", Simbolo="BAM")
db.session.add(ci)

cj = Monedas(Nombre="Naira Nigeriana", Simbolo="NGN")
db.session.add(cj)

ck = Monedas(Nombre="Nuevo Rublo Bielorruso", Simbolo="BYN")
db.session.add(ck)

cl = Monedas(Nombre="Nuevo Sequel Israeli", Simbolo="ILS")
db.session.add(cl)

cm = Monedas(Nombre="Sol Peruano", Simbolo="PEN")
db.session.add(cm)

cn = Monedas(Nombre="Peso Argentino", Simbolo="ARS")
db.session.add(cn)

co = Monedas(Nombre="Peso Chileno", Simbolo="CLP")
db.session.add(co)

cp = Monedas(Nombre="Peso Colombiano", Simbolo="COP")
db.session.add(cp)

cq = Monedas(Nombre="Peso Cubano", Simbolo="CUP")
db.session.add(cq)

cr = Monedas(Nombre="Peso Cubano Convertible", Simbolo="CUC")
db.session.add(cr)

cs = Monedas(Nombre="Peso Dominicano", Simbolo="DOP")
db.session.add(cs)

ct = Monedas(Nombre="Peso Filipino", Simbolo="PHP")
db.session.add(ct)

cu = Monedas(Nombre="Peso Mexicano", Simbolo="MXN")
db.session.add(cu)

cv = Monedas(Nombre="Peso Uruguayo", Simbolo="UYU")
db.session.add(cv)

cw = Monedas(Nombre="Quetzal", Simbolo="GTQ")
db.session.add(cw)

cx = Monedas(Nombre="Rand Sudafricano", Simbolo="ZAR")
db.session.add(cx)

cy = Monedas(Nombre="Real", Simbolo="BRL")
db.session.add(cy)

cz = Monedas(Nombre="Rial Yemeni", Simbolo="YER")
db.session.add(cz)

da = Monedas(Nombre="Riel Camboyano", Simbolo="KHR")
db.session.add(da)

dbul = Monedas(Nombre="Ringgit Malayo", Simbolo="MYR")
db.session.add(dbul)

dc = Monedas(Nombre="Riyal Saudi", Simbolo="SAR")
db.session.add(dc)

dd = Monedas(Nombre="Rublo Ruso", Simbolo="RUB")
db.session.add(dd)

de = Monedas(Nombre="Rupia India", Simbolo="INR")
db.session.add(de)

df = Monedas(Nombre="Rupia de Indonesia", Simbolo="IDR")
db.session.add(df)

dg = Monedas(Nombre="Rupia Pakistani", Simbolo="PKR")
db.session.add(dg)

dh = Monedas(Nombre="Rupia de Maldivas", Simbolo="MVR")
db.session.add(dh)

di = Monedas(Nombre="Rupia de Nepal", Simbolo="NPR")
db.session.add(di)

do = Monedas(Nombre="Rupia de Sri Lanka", Simbolo="LKR")
db.session.add(do)

dj = Monedas(Nombre="Taka Bangladesi", Simbolo="BDT")
db.session.add(dj)

dk = Monedas(Nombre="Tugrik Mongol", Simbolo="MNT")
db.session.add(dk)

dl = Monedas(Nombre="Won Norcoreano", Simbolo="KPW")
db.session.add(dl)

dm = Monedas(Nombre="Won Surcoreano", Simbolo="KRW")
db.session.add(dm)

dn = Monedas(Nombre="Yen", Simbolo="JPY")
db.session.add(dn)

dq = Monedas(Nombre="Yuan Chino", Simbolo="CNY")
db.session.add(dq)

db.session.commit()