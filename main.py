from flask import Flask, render_template, url_for, request, send_from_directory, session, escape, redirect
import uuid
from werkzeug.utils import secure_filename
from models import User, db, Cita
import hashlib
import os
from calendar import monthcalendar
from datetime import date, datetime
from auxiliar import previous_month, next_month, imprime_mes, allowed_file, current_month, convierte_hora


UPLOAD_FOLDER = os.path.abspath("./static/img/")


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  # diccionario de configuración de la aplicación
app.secret_key = "123secreto"

db.create_all() # Crea las tablas de la base de datos si no existe

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user_name = request.form.get("user-name")
        user_password = request.form.get("user-password")   # contraseña en texto plano
        user_password = hashlib.sha256(user_password.encode()).hexdigest()    # contraseña encriptada

        user = db.query(User).filter_by(username=user_name, password=user_password).first()
        if user:
            session["username"] = user.username

            return redirect("calendario")
        else:
            return "El usuario no existe"




@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")  # contraseña en texto plano
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # contraseña encriptada
        name = request.form.get("name")
        surname = request.form.get("surname")
        birthdate = datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d")    # en MAC no funciona con Safari
        email = request.form.get("email")
        f_imagen = request.files["img_file"]
        if f_imagen.filename == "":  # no se ha cargado imagen
            pass
        else:
            if allowed_file(f_imagen.filename):
                filename = str(uuid.uuid4()) + secure_filename(f_imagen.filename)    #para asegurar que no hay dos nombres iguales
                f_imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                user = User(username=username, password=hashed_password, name=name, surname=surname, birthdate=birthdate, email=email, photo=filename)

                db.add(user)
                db.commit()

        return render_template("login.html")



@app.route("/calendario", methods=["POST", "GET"])
def calendario():

    if request.method == "GET":

        if "username" in session:
            t_month = request.args.get('month')  # creo que es de tipo string
            t_year = request.args.get('year')
            action = request.args.get('action')
            user = db.query(User).filter_by(username=session["username"]).first()
            url_imagen = "../static/img/" + user.photo

            if t_month and t_year and action:
                if action == "previous":
                    month, year = previous_month(t_month, t_year)
                    calendario_mes = monthcalendar(year, month)
                elif action == "next":
                    month, year = next_month(t_month, t_year)
                    calendario_mes = monthcalendar(year, month)
                elif action == "current":
                    month, year = current_month(t_month, t_year)
                    calendario_mes = monthcalendar(year, month)
            else:
                month = date.today().month
                year = date.today().year
                calendario_mes = monthcalendar(year, month)

            user = db.query(User).filter_by(username=session["username"]).first()
            citas = db.query(Cita).filter_by(user_id=user.id).all()  # obtengo todas las citas, pero deberían ser las de ese día

            citas_mes = []

            for cita in citas:  # guardo en citas_mes todas las citas del mes
                if cita.fecha.year == year and cita.fecha.month == month:
                    citas_mes.append(cita)

            dias = []
            for cita in citas_mes:
                dias.append(cita.fecha.day)

            return render_template("calendario.html", calendario_mes=calendario_mes, month=month, year=year,
                               text_month=imprime_mes(month), username=user.username, url_imagen=url_imagen, dias_cita=dias)

        else:
            return "No estás logueado"


@app.route("/dia", methods=["POST", "GET"])
def dia():

    if request.method == "GET":
        if "username" in session:
            t_month = request.args.get('month')  # creo que es de tipo string
            t_year = request.args.get('year')
            t_day = request.args.get('day')
            month, year = current_month(t_month, t_year)
            # calendario_mes = monthcalendar(year, month)

            user = db.query(User).filter_by(username=session["username"]).first()
            citas = db.query(Cita).filter_by(user_id=user.id).all()   # obtengo todas las citas, pero deberían ser las de ese día

            cita_dia = []
            print(citas)
            for cita in citas:
                if cita.fecha.year == int(t_year) and cita.fecha.month == int(t_month) and cita.fecha.day == int(t_day):
                    cita_dia.append(cita)

            return render_template("dia.html", month=t_month, year=t_year, day=t_day, text_month=imprime_mes(month), citas_dia=cita_dia)
        else:
            pass
    elif register.method == "POST":
        pass


@app.route("/add_dia", methods=["POST"])
def add_dia():

    t_hora_cita = request.form.get("hora_cita")
    titulo_cita = request.form.get("titulo_cita")
    notas_cita = request.form.get("notas_cita")
    year = request.form.get("cita_year")
    month = request.form.get("cita_month")
    day = request.form.get("cita_day")

    hora, minutos = convierte_hora(t_hora_cita)
    t_cita = year + "-" + month + "-" + day + "-" + hora + "-" + minutos
    hora_cita = datetime.strptime(t_cita, "%Y-%m-%d-%H-%M") # convierto del formato texto al datetime

    user = db.query(User).filter_by(username=session["username"]).first()

    cita = Cita(fecha=hora_cita, titulo=titulo_cita, notas=notas_cita, user_id=user.id)

    db.add(cita)
    db.commit()


    return redirect(url_for('dia', month=month, year=year, day=day))


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop('username')

    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
