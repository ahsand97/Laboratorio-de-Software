(Recomendable usar Entorno Virtual)

-----------------------------------------------------
-Instalar requerimientos
 pip install -r requirements.txt
 
------------------------------------------------------
-La primer vez de uso

SET FLASK_APP=Proyecto.py
flask db init
flask db migrate
flask db upgrade

python monedas.py
python llenarbase.py

flask run
------------------------------------------------------

-Uso

SET FLASK_APP= Proyecto.py

flask run
