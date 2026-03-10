import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ---------- CONFIGURACION CORREO ----------
remitente = "brahianvelez66@gmail.com"
password = "myeslfrkrjpslulq"

# ---------- FUNCION PARA ENVIAR CORREO ----------
def enviar_correo(destinatario, actividad, sede, maquina):

    mensaje = f"""
Nueva actividad asignada

Actividad: {actividad}
Sede: {sede}
Maquina: {maquina}
Fecha: {datetime.today().strftime("%d/%m/%Y")}
"""

    msg = MIMEText(mensaje)

    msg["Subject"] = "Nueva actividad asignada"
    msg["From"] = remitente
    msg["To"] = destinatario

    servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    servidor.login(remitente, password)
    servidor.send_message(msg)
    servidor.quit()

# ---------- CONEXION GOOGLE SHEETS ----------

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("SISTEMA ACTIVIDADES")

actividades_sheet = sheet.worksheet("ACTIVIDADES")
ejecuciones_sheet = sheet.worksheet("EJECUCIONES")
trabajadores_sheet = sheet.worksheet("TRABAJADORES")

actividades = actividades_sheet.get_all_records()
ejecuciones = ejecuciones_sheet.get_all_records()
trabajadores = trabajadores_sheet.get_all_records()

hoy = datetime.today().date()

print("Fecha:", hoy)

for act in actividades:

    fecha_inicio = datetime.strptime(act["FECHA_INICIO"], "%d/%m/%Y").date()
    fecha_fin = datetime.strptime(act["FECHA_FIN"], "%d/%m/%Y").date()

    frecuencia = int(act["FRECUENCIA"])
    tipo = act["TIPO"]

    if fecha_inicio <= hoy <= fecha_fin:

        if tipo == "DIAS":

            diferencia = (hoy - fecha_inicio).days

            if diferencia % frecuencia == 0:

                id_ejec = "EJ" + str(len(ejecuciones) + 1).zfill(3)

                nueva_ejecucion = [
                    id_ejec,
                    act["ID_ACT"],
                    act["SEDE"],
                    act["MAQUINA"],
                    hoy.strftime("%d/%m/%Y"),
                    "PENDIENTE",
                    0
                ]

                ejecuciones_sheet.append_row(nueva_ejecucion)

                responsable = act["RESPONSABLE"]

                for t in trabajadores:

                    if t["ID_TRAB"] == responsable:

                        try:
                            enviar_correo(
                                t["CORREO"],
                                act["ACTIVIDAD"],
                                act["SEDE"],
                                act["MAQUINA"]
                            )
                            print("Correo enviado correctamente")

                        except Exception as error:
                            print("No se pudo enviar correo:", error)

                print("Ejecución creada:", id_ejec)