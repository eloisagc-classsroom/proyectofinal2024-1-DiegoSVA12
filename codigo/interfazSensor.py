import tkinter as tk
from serial import Serial
import time

# Configura la conexión serial con el módulo Bluetooth conectado al Arduino
arduino = Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)  # Da tiempo para que la conexión se establezca

# Variables para controlar el intervalo de actualización y modos
update_interval = 10000  # Intervalo de actualización en milisegundos
is_manual_mode = False
is_night_mode = False

def actualizar_distancia():
    try:
        # Leer y procesar datos desde el Arduino
        arduino.flushInput()  # Limpiar el buffer de entrada
        arduino.write(b'g')  # Enviar señal para obtener datos
        time.sleep(0.1)  # Esperar la respuesta del Arduino
        data = arduino.readline().decode().strip()
        
        if data:
            # Procesar los datos recibidos y actualizar la interfaz gráfica
            distancias = data.split(',')
            if len(distancias) == 3:
                distancia1 = float(distancias[0])
                distancia2 = float(distancias[1])
                distancia3 = float(distancias[2])

                # Actualizar la información y la visualización de los sensores
                porcentaje1 = calcular_porcentaje(distancia1)
                sensor1_label.config(
                    text=f"Sensor 1: {distancia1:.2f} cm\nLlenado: {porcentaje1:.0%}")
                actualizar_rectangulo(sensor1_canvas, porcentaje1, color1.get())
                verificar_alerta(porcentaje1, alerta1_label)

                porcentaje2 = calcular_porcentaje(distancia2)
                sensor2_label.config(
                    text=f"Sensor 2: {distancia2:.2f} cm\nLlenado: {porcentaje2:.0%}")
                actualizar_rectangulo(sensor2_canvas, porcentaje2, color2.get())
                verificar_alerta(porcentaje2, alerta2_label)

                porcentaje3 = calcular_porcentaje(distancia3)
                sensor3_label.config(
                    text=f"Sensor 3: {distancia3:.2f} cm\nLlenado: {porcentaje3:.0%}")
                actualizar_rectangulo(sensor3_canvas, porcentaje3, color3.get())
                verificar_alerta(porcentaje3, alerta3_label)

    except Exception as e:
        # Manejo de errores
        sensor1_label.config(text=f"Sensor 1: Error: {e}")
        sensor2_label.config(text=f"Sensor 2: Error: {e}")
        sensor3_label.config(text=f"Sensor 3: Error: {e}")

    # Configurar la próxima actualización si no está en modo manual
    if not is_manual_mode:
        root.after(update_interval, actualizar_distancia)

def calcular_porcentaje(distancia):
    # Calcular el porcentaje de llenado basado en la distancia medida
    if distancia >= 21:
        return 0.0
    elif distancia <= 9:
        return 1.0
    else:
        return (21 - distancia) / 12

def verificar_alerta(porcentaje, alerta_label):
    # Verificar si el porcentaje de llenado está por debajo del umbral y mostrar una alerta
    if porcentaje <= 0.1:
        alerta_label.config(text="ALERTA: Nivel muy bajo", fg="red")
    else:
        alerta_label.config(text="", fg="black")

def refrescar():
    # Función para refrescar manualmente los datos
    actualizar_distancia()

def on_closing():
    # Cerrar la conexión serial y destruir la ventana al cerrar la aplicación
    arduino.close()
    root.destroy()

def actualizar_rectangulo(canvas, porcentaje, color):
    # Actualizar la visualización del llenado en el canvas
    canvas.delete("all")
    canvas.create_rectangle(50, 50, 150, 150, outline="black", width=2)
    canvas.create_rectangle(50, 150 - 100 * porcentaje, 150, 150, fill=color)

def actualizar_color(*args):
    # Función para actualizar los datos cuando cambia el color seleccionado
    actualizar_distancia()

def cambiar_intervalo(*args):
    # Cambiar el intervalo de actualización o activar el modo manual
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
    # Alternar entre modo nocturno y modo diurno
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

# Configuración de la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Lector de Distancia Ultrasónica")

# Crear marcos para organizar los sensores
sensor_frame = tk.Frame(root)
sensor_frame.pack(pady=10)

# Colores disponibles para los recipientes
colores = ["blue", "green", "red", "yellow", "purple"]

# Configuración y visualización del sensor 1
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

# Configuración y visualización del sensor 2
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

# Configuración y visualización del sensor 3
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

# Configuración del intervalo de actualización con una lista desplegable
intervalos = [str(i) for i in range(5, 16)] + ["Manual"]
intervalo_var = tk.StringVar(value=intervalos[0])
intervalo_var.trace("w", cambiar_intervalo)

intervalo_frame = tk.Frame(root)
intervalo_frame.pack(pady=10)
intervalo_label = tk.Label(intervalo_frame, text="Intervalo de actualización: ", font=('Helvetica', 12))
intervalo_label.pack(side=tk.LEFT)
intervalo_menu = tk.OptionMenu(intervalo_frame, intervalo_var, *intervalos)
intervalo_menu.pack(side=tk.LEFT, padx=5)

# Botón para alternar entre modo diurno y nocturno
night_mode_button = tk.Button(root, text="Modo Noche", command=toggle_night_mode)
night_mode_button.pack(pady=10)

# Botón para refrescar manualmente los datos
refrescar_button = tk.Button(root, text="Refrescar", command=refrescar)
refrescar_button.pack(pady=10)

# Manejo del cierre de la ventana para cerrar la conexión serial
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la primera actualización automática
root.after(update_interval, actualizar_distancia)

# Iniciar el bucle principal de Tkinter
root.mainloop()
