import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("SISTEMA ACTIVIDADES")

ejecuciones_sheet = sheet.worksheet("EJECUCIONES")

ejecuciones = ejecuciones_sheet.get_all_records()

hoy = datetime.today().date()

for i, e in enumerate(ejecuciones):

    fecha = datetime.strptime(e["FECHA"], "%d/%m/%Y").date()
    estado = e["ESTADO"]

    if estado == "PENDIENTE" and fecha < hoy:

        fila = i + 2

        ejecuciones_sheet.update_cell(fila, 6, "ATRASADA")

        print("Actividad atrasada:", e["ID_EJEC"])