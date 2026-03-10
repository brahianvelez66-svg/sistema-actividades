import os

print("Ejecutando motor de actividades...")
os.system("python motor_actividades.py")

print("Actualizando ejecuciones desde formulario...")
os.system("python actualizar_ejecuciones.py")

print("Revisando actividades atrasadas...")
os.system("python control_atrasos.py")

print("Sistema ejecutado correctamente")