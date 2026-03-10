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

form_sheet = sheet.worksheet("RESPUESTAS_ACTIVIDADES")
actividades_sheet = sheet.worksheet("ACTIVIDADES")

respuestas = form_sheet.get_all_records()
actividades = actividades_sheet.get_all_records()

contador = len(actividades) + 1

for i, r in enumerate(respuestas):

    r = {k.strip(): v for k, v in r.items()}

    # revisar si ya fue cargada
    if r.get("CARGADA") == "SI":
        continue

    tipo_objeto = r["TIPO_OBJETO"]
    sede = r["SEDE"]
    maquina = r["MAQUINA"]
    responsable = r["RESPONSABLE"]
    actividad = r["ACTIVIDAD"]
    fecha_inicio = r["FECHA_INICIO"]
    fecha_fin = r["FECHA_FIN"]
    frecuencia = r["FRECUENCIA"]
    tipo = r["TIPO"]

    if tipo_objeto == "SEDE":
        maquina = ""

    id_act = "ACT" + str(contador).zfill(3)

    nueva_actividad = [
        id_act,
        tipo_objeto,
        sede,
        maquina,
        responsable,
        actividad,
        fecha_inicio,
        fecha_fin,
        frecuencia,
        tipo
    ]

    actividades_sheet.append_row(nueva_actividad)

    # marcar como cargada
    fila = i + 2
    col = len(r) + 1
    form_sheet.update_cell(fila, col, "SI")

    print("Actividad creada:", id_act)

    contador += 1