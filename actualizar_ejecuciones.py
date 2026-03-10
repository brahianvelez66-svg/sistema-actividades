import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("SISTEMA ACTIVIDADES")

respuestas_sheet = sheet.worksheet("RESPUESTAS_FORM")
ejecuciones_sheet = sheet.worksheet("EJECUCIONES")

respuestas = respuestas_sheet.get_all_records()
ejecuciones = ejecuciones_sheet.get_all_records()

for r in respuestas:

    # limpiar espacios en nombres de columnas
    r = {k.strip(): v for k, v in r.items()}

    id_ejec = r["ID_EJECUCION"]
    resultado = r["¿SE REALIZÓ LA ACTIVIDAD?"]

    for i, e in enumerate(ejecuciones):

        if e["ID_EJEC"] == id_ejec:

            fila = i + 2

            if resultado == "SI":
                ejecuciones_sheet.update_cell(fila, 6, "REALIZADA")

            if resultado == "NO":
                ejecuciones_sheet.update_cell(fila, 6, "PENDIENTE")

            print("Ejecución actualizada:", id_ejec)




