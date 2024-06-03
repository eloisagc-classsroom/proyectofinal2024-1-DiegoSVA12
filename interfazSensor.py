import tkinter as tk
from serial import Serial
import time

# Configura la conexión serial
# Cambia 'COM5' o '/dev/tty.HC-05-DevB' por el puerto correcto de tu módulo Bluetooth
arduino = Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)  # Da tiempo para que la conexión se establezca

# Variables para el intervalo de actualización
update_interval = 10000  # Intervalo de actualización en milisegundos
is_manual_mode = False
is_night_mode = False

def actualizar_distancia():
    try:
        arduino.flushInput()  # Limpiar el buffer de entrada
        arduino.write(b'g')
        time.sleep(0.1)  # Esperar para asegurar que Arduino responda
        data = arduino.readline().decode().strip()
        if data:
            distancias = data.split(',')
            if len(distancias) == 3:
                distancia1 = float(distancias[0])
                distancia2 = float(distancias[1])
                distancia3 = float(distancias[2])

                # Calcular el porcentaje de llenado para el sensor 1
                porcentaje1 = calcular_porcentaje(distancia1)
                sensor1_label.config(
                    text=f"Sensor 1: {distancia1:.2f} cm\nLlenado: {porcentaje1:.0%}")
                actualizar_rectangulo(sensor1_canvas, porcentaje1, color1.get())
                verificar_alerta(porcentaje1, alerta1_label)

                # Calcular el porcentaje de llenado para el sensor 2
                porcentaje2 = calcular_porcentaje(distancia2)
                sensor2_label.config(
                    text=f"Sensor 2: {distancia2:.2f} cm\nLlenado: {porcentaje2:.0%}")
                actualizar_rectangulo(sensor2_canvas, porcentaje2, color2.get())
                verificar_alerta(porcentaje2, alerta2_label)

                # Calcular el porcentaje de llenado para el sensor 3
                porcentaje3 = calcular_porcentaje(distancia3)
                sensor3_label.config(
                    text=f"Sensor 3: {distancia3:.2f} cm\nLlenado: {porcentaje3:.0%}")
                actualizar_rectangulo(sensor3_canvas, porcentaje3, color3.get())
                verificar_alerta(porcentaje3, alerta3_label)

    except Exception as e:
        sensor1_label.config(text=f"Sensor 1: Error: {e}")
        sensor2_label.config(text=f"Sensor 2: Error: {e}")
        sensor3_label.config(text=f"Sensor 3: Error: {e}")

    # Configurar la próxima actualización en el intervalo especificado si no está en modo manual
    if not is_manual_mode:
        root.after(update_interval, actualizar_distancia)

def calcular_porcentaje(distancia):
    if distancia >= 21:
        return 0.0
    elif distancia <= 9:
        return 1.0
    else:
        return (21 - distancia) / 12

def verificar_alerta(porcentaje, alerta_label):
    if porcentaje <= 0.1:
        alerta_label.config(text="ALERTA: Nivel muy bajo", fg="red")
    else:
        alerta_label.config(text="", fg="black")

def refrescar():
    actualizar_distancia()

def on_closing():
    arduino.close()
    root.destroy()

def actualizar_rectangulo(canvas, porcentaje, color):
    canvas.delete("all")
    canvas.create_rectangle(50, 50, 150, 150, outline="black", width=2)
    canvas.create_rectangle(50, 150 - 100 * porcentaje, 150, 150, fill=color)

def actualizar_color(*args):
    actualizar_distancia()

def cambiar_intervalo(*args):
    global update_interval, is_manual_mode
    valor = intervalo_var.get()
    if valor == "Manual":
        is_manual_mode = True
    else:
        is_manual_mode = False
        update_interval = int(valor) * 1000
        if not is_manual_mode:
            root.after(update_interval, actualizar_distancia)

def toggle_night_mode():
    global is_night_mode
    is_night_mode = not is_night_mode
    if is_night_mode:
        root.config(bg="black")
        sensor_frame.config(bg="black")
        for widget in sensor_frame.winfo_children():
            widget.config(bg="black", fg="white")
        night_mode_button.config(text="Modo Día", bg="black", fg="white")
    else:
        root.config(bg="white")
        sensor_frame.config(bg="white")
        for widget in sensor_frame.winfo_children():
            widget.config(bg="white", fg="black")
        night_mode_button.config(text="Modo Noche", bg="white", fg="black")

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Lector de Distancia Ultrasónica")

# Configuración de los marcos para los sensores
sensor_frame = tk.Frame(root)
sensor_frame.pack(pady=10)

# Colores disponibles para los recipientes
colores = ["blue", "green", "red", "yellow", "purple"]

# Configuración del sensor 1
sensor1_frame = tk.Frame(sensor_frame)
sensor1_frame.pack(side=tk.LEFT, padx=10)
sensor1_label = tk.Label(sensor1_frame, text="", font=('Helvetica', 18))
sensor1_label.pack(pady=10)
sensor1_canvas = tk.Canvas(sensor1_frame, width=200, height=200)
sensor1_canvas.pack()
color1 = tk.StringVar(value="blue")
color1.trace("w", actualizar_color)
color1_menu = tk.OptionMenu(sensor1_frame, color1, *colores)
color1_menu.pack(pady=10)
alerta1_label = tk.Label(sensor1_frame, text="", font=('Helvetica', 12))
alerta1_label.pack(pady=5)

# Configuración del sensor 2
sensor2_frame = tk.Frame(sensor_frame)
sensor2_frame.pack(side=tk.LEFT, padx=10)
sensor2_label = tk.Label(sensor2_frame, text="", font=('Helvetica', 18))
sensor2_label.pack(pady=10)
sensor2_canvas = tk.Canvas(sensor2_frame, width=200, height=200)
sensor2_canvas.pack()
color2 = tk.StringVar(value="blue")
color2.trace("w", actualizar_color)
color2_menu = tk.OptionMenu(sensor2_frame, color2, *colores)
color2_menu.pack(pady=10)
alerta2_label = tk.Label(sensor2_frame, text="", font=('Helvetica', 12))
alerta2_label.pack(pady=5)

# Configuración del sensor 3
sensor3_frame = tk.Frame(sensor_frame)
sensor3_frame.pack(side=tk.LEFT, padx=10)
sensor3_label = tk.Label(sensor3_frame, text="", font=('Helvetica', 18))
sensor3_label.pack(pady=10)
sensor3_canvas = tk.Canvas(sensor3_frame, width=200, height=200)
sensor3_canvas.pack()
color3 = tk.StringVar(value="blue")
color3.trace("w", actualizar_color)
color3_menu = tk.OptionMenu(sensor3_frame, color3, *colores)
color3_menu.pack(pady=10)
alerta3_label = tk.Label(sensor3_frame, text="", font=('Helvetica', 12))
alerta3_label.pack(pady=5)

# Configuración del intervalo de actualización
intervalos = [str(i) for i in range(5, 16)] + ["Manual"]
intervalo_var = tk.StringVar(value=intervalos[0])
intervalo_var.trace("w", cambiar_intervalo)

intervalo_frame = tk.Frame(root)
intervalo_frame.pack(pady=10)
intervalo_label = tk.Label(intervalo_frame, text="Intervalo de actualización: ", font=('Helvetica', 12))
intervalo_label.pack(side=tk.LEFT)
intervalo_menu = tk.OptionMenu(intervalo_frame, intervalo_var, *intervalos)
intervalo_menu.pack(side=tk.LEFT, padx=5)

# Botón para modo nocturno
night_mode_button = tk.Button(root, text="Modo Noche", command=toggle_night_mode)
night_mode_button.pack(pady=10)

# Botón para refrescar
refrescar_button = tk.Button(root, text="Refrescar", command=refrescar)
refrescar_button.pack(pady=10)

# Manejar el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la primera actualización
root.after(update_interval, actualizar_distancia)

root.mainloop()
