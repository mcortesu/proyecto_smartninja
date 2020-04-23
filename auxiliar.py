from datetime import datetime

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge", "gif"])

# comprueba la extensión, para ello comprueba si hay un . y luego divide la cadena en el primer punto
# y coge la parte derecha
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

# se recibe una cadena al estilo 1:23 PM o 12:01 AM y se saca la hora y minutos
def convierte_hora(cadena_hora):

    hora = cadena_hora.rsplit(":", 1)[0]    # de 1:23 PM lo divido en 2 por : y cojo la parte izquierda
    aux = cadena_hora.rsplit(":", 1)[1]
    minutos = aux.rsplit(" ", 1)[0] # de 23 PM lo divido en 2 por el espacio y cojo la izquierda
    franja = aux.rsplit(" ", 1)[1]  # cojo el AM o PM

    if int(hora) < 12 and franja == "PM":
        i_hora = int(hora) + 12
    elif int(hora) == 12 and franja == "AM":
        i_hora = 0

    return str(i_hora), minutos

def next_month(t_month, t_year):
    month = int(t_month)
    year = int(t_year)

    if month == 12:
        return 1, year+1
    else:
        return month+1, year


def previous_month(t_month, t_year):
    month = int(t_month)
    year = int(t_year)

    if month == 1:
        return 12, year-1
    else:
        return month-1, year

def current_month(t_month, t_year):
    month = int(t_month)
    year = int(t_year)

    return month, year

def imprime_mes(mes):
    if mes == 1:
        t_mes = "Enero"
    elif mes == 2:
        t_mes = "Febrero"
    elif mes == 3:
        t_mes = "Marzo"
    elif mes == 4:
        t_mes = "Abril"
    elif mes == 5:
        t_mes = "Mayo"
    elif mes == 6:
        t_mes = "Junio"
    elif mes == 7:
        t_mes = "Julio"
    elif mes == 8:
        t_mes = "Agosto"
    elif mes == 9:
        t_mes = "Septiembre"
    elif mes == 10:
        t_mes = "Octubre"
    elif mes == 11:
        t_mes = "Noviembre"
    elif mes == 12:
        t_mes = "Diciembre"

    return t_mes
