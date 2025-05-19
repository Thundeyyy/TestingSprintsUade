import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re

# Nombre del archivo para guardar las tareas
ARCHIVO_TAREAS = "tareas.json"

def cargar_tareas():
    """Carga las tareas desde el archivo JSON."""
    if os.path.exists(ARCHIVO_TAREAS):
        with open(ARCHIVO_TAREAS, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON."""
    with open(ARCHIVO_TAREAS, "w") as f:
        json.dump(tareas, f)

def validar_caracteres(texto):
    """Valida que el texto solo contenga caracteres permitidos."""
    caracteres_permitidos = r'^[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ,.;:¿?¡!\-_()\"\' \n]+$'
    if not re.match(caracteres_permitidos, texto):
        caracteres_prohibidos = re.findall(r'[<>\[\]{}|\\@#$%^&*~+=`]', texto)
        if caracteres_prohibidos:
            messagebox.showwarning("Advertencia", 
                                 f"Caracteres no permitidos: {' '.join(set(caracteres_prohibidos))}")
            return False
    return True

def validar_tarea(titulo, descripcion=""):
    """Valida el título y la descripción de la tarea."""
    titulo = titulo.strip()
    
    if not titulo:
        messagebox.showwarning("Advertencia", "El título es obligatorio.")
        return False
    if len(titulo) > 50:
        messagebox.showwarning("Advertencia", "Máximo 50 caracteres para el título.")
        return False
    if not validar_caracteres(titulo):
        return False
    if descripcion and not validar_caracteres(descripcion):
        return False
    if len(descripcion) > 200:
        messagebox.showwarning("Advertencia", "Máximo 200 caracteres para la descripción.")
        return False
    return True

def mostrar_formulario_agregar():
    """Muestra el formulario para agregar una nueva tarea."""
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Agregar Nueva Tarea")
    dialogo.geometry("400x300")
    
    # Configurar el grid para que sea expansible
    dialogo.grid_columnconfigure(1, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    
    # Frame principal para el contenido
    frame_contenido = tk.Frame(dialogo)
    frame_contenido.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    frame_contenido.grid_columnconfigure(1, weight=1)
    
    etiqueta_titulo = tk.Label(frame_contenido, text="Título:")
    etiqueta_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entrada_titulo = tk.Entry(frame_contenido)
    entrada_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    etiqueta_descripcion = tk.Label(frame_contenido, text="Descripción:")
    etiqueta_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entrada_descripcion = tk.Text(frame_contenido, height=5)
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    # Frame para los botones
    frame_botones = tk.Frame(dialogo)
    frame_botones.grid(row=1, column=0, columnspan=2, pady=10, sticky="s")
    
    def guardar_nueva_tarea():
        titulo = entrada_titulo.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        if validar_tarea(titulo, descripcion):
            nueva_tarea = {
                "titulo": titulo,
                "descripcion": descripcion,
                "completada": False
            }
            tareas.append(nueva_tarea)
            guardar_tareas(tareas)
            actualizar_lista_tareas()
            dialogo.destroy()
    
    def cancelar_agregar():
        dialogo.destroy()
    
    boton_guardar = tk.Button(frame_botones, text="Guardar", command=guardar_nueva_tarea)
    boton_guardar.pack(side=tk.LEFT, padx=5)
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar_agregar)
    boton_cancelar.pack(side=tk.LEFT, padx=5)
    
    dialogo.transient(ventana)
    dialogo.grab_set()
    ventana.wait_window(dialogo)

def mostrar_formulario_editar(indice):
    """Muestra el formulario para editar una tarea existente."""
    if tareas[indice]['completada']:
        messagebox.showwarning("Advertencia", "La tarea necesita estar en estado no completado para poder editar.")
        return
    
    tarea = tareas[indice]
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Editar Tarea")
    dialogo.geometry("400x300")
    
    # Configurar el grid para que sea expansible
    dialogo.grid_columnconfigure(1, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    
    # Frame principal para el contenido
    frame_contenido = tk.Frame(dialogo)
    frame_contenido.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    frame_contenido.grid_columnconfigure(1, weight=1)
    
    etiqueta_titulo = tk.Label(frame_contenido, text="Título:")
    etiqueta_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entrada_titulo = tk.Entry(frame_contenido)
    entrada_titulo.insert(0, tarea['titulo'])
    entrada_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    etiqueta_descripcion = tk.Label(frame_contenido, text="Descripción:")
    etiqueta_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entrada_descripcion = tk.Text(frame_contenido, height=5)
    entrada_descripcion.insert("1.0", tarea['descripcion'])
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    # Frame para los botones
    frame_botones = tk.Frame(dialogo)
    frame_botones.grid(row=1, column=0, columnspan=2, pady=10, sticky="s")
    
    def actualizar_tarea():
        titulo = entrada_titulo.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        if validar_tarea(titulo, descripcion):
            tareas[indice]['titulo'] = titulo
            tareas[indice]['descripcion'] = descripcion
            guardar_tareas(tareas)
            actualizar_lista_tareas()
            # Resaltar la tarea editada brevemente
            resaltar_tarea(indice)
            dialogo.destroy()
            messagebox.showinfo("Información", "Tarea actualizada correctamente.")
    
    def cancelar_editar():
        dialogo.destroy()
    
    boton_actualizar = tk.Button(frame_botones, text="Actualizar", command=actualizar_tarea)
    boton_actualizar.pack(side=tk.LEFT, padx=5)
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar_editar)
    boton_cancelar.pack(side=tk.LEFT, padx=5)
    
    dialogo.transient(ventana)
    dialogo.grab_set()
    ventana.wait_window(dialogo)

def resaltar_tarea(indice):
    """Resalta brevemente una tarea después de ser editada."""
    for widget in frame_lista.winfo_children()[indice].winfo_children():
        if isinstance(widget, tk.Checkbutton) or widget['text'] == tareas[indice]['titulo']:
            widget.config(bg='#b3e6b3')  # Color verde claro para resaltar
            frame_lista.after(1000, lambda w=widget: w.config(bg='#e6f2ff' if not tareas[indice]['completada'] else '#f0f0f0'))

def confirmar_eliminar(indice):
    """Muestra un diálogo de confirmación antes de eliminar una tarea."""
    tarea = tareas[indice]
    respuesta = messagebox.askyesno("Confirmar",
                                 f"¿Eliminar esta tarea?\n\"{tarea['titulo']}\"\nEsta acción no se puede deshacer.")
    if respuesta:
        del tareas[indice]
        guardar_tareas(tareas)
        actualizar_lista_tareas()

def mostrar_detalles_tarea(tarea):
    """Muestra una ventana con los detalles de la tarea seleccionada."""
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Detalles de la Tarea")
    dialogo.geometry("400x300")
    
    # Configurar el grid
    dialogo.grid_columnconfigure(1, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    
    # Frame para el contenido
    frame_contenido = tk.Frame(dialogo)
    frame_contenido.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    
    # Estado
    estado = "Completada" if tarea['completada'] else "Pendiente"
    etiqueta_estado = tk.Label(frame_contenido, text=f"Estado: {estado}", font=("Arial", 10, "bold"))
    etiqueta_estado.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    # Título
    etiqueta_titulo = tk.Label(frame_contenido, text="Título:", font=("Arial", 10, "bold"))
    etiqueta_titulo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    texto_titulo = tk.Label(frame_contenido, text=tarea['titulo'], wraplength=300)
    texto_titulo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # Descripción
    etiqueta_descripcion = tk.Label(frame_contenido, text="Descripción:", font=("Arial", 10, "bold"))
    etiqueta_descripcion.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    texto_descripcion = tk.Label(frame_contenido, text=tarea['descripcion'], wraplength=300)
    texto_descripcion.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    # Botón cerrar
    boton_cerrar = tk.Button(dialogo, text="Cerrar", command=dialogo.destroy)
    boton_cerrar.grid(row=3, column=0, pady=10)
    
    dialogo.transient(ventana)
    dialogo.grab_set()
    ventana.wait_window(dialogo)

def toggle_completada(indice):
    """Alterna el estado de completada de una tarea."""
    tareas[indice]['completada'] = not tareas[indice]['completada']
    guardar_tareas(tareas)
    actualizar_lista_tareas()

def calcular_estadisticas():
    """Calcula las estadísticas de las tareas."""
    total_tareas = len(tareas)
    tareas_completadas = sum(1 for tarea in tareas if tarea['completada'])
    tareas_pendientes = total_tareas - tareas_completadas
    porcentaje = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
    return {
        'total': total_tareas,
        'completadas': tareas_completadas,
        'pendientes': tareas_pendientes,
        'porcentaje': porcentaje
    }

def actualizar_estadisticas():
    """Actualiza la visualización de las estadísticas."""
    stats = calcular_estadisticas()
    
    # Actualizar etiquetas
    label_total.config(text=f"Total de Tareas: {stats['total']}")
    label_completadas.config(text=f"Tareas Completadas: {stats['completadas']}")
    label_pendientes.config(text=f"Tareas Pendientes: {stats['pendientes']}")
    label_porcentaje.config(text=f"Porcentaje de Avance: {stats['porcentaje']:.1f}%")
    
    # Actualizar barra de progreso
    barra_progreso['value'] = stats['porcentaje']

def actualizar_lista_tareas():
    """Actualiza la visualización de la lista de tareas."""
    for widget in frame_lista.winfo_children():
        widget.destroy()

    if not tareas:
        label_vacio = tk.Label(frame_lista, text="No hay tareas creadas.", fg="gray")
        label_vacio.pack(pady=10)
    else:
        for i, tarea in enumerate(tareas):
            frame_tarea = tk.Frame(frame_lista)
            frame_tarea.pack(fill=tk.X, padx=5, pady=2)
            
            # Checkbox para estado completado con símbolo ✓
            var_check = tk.BooleanVar(value=tarea['completada'])
            checkbox = tk.Checkbutton(frame_tarea, 
                                    variable=var_check,
                                    command=lambda idx=i: toggle_completada(idx),
                                    indicatoron=False,
                                    width=2,
                                    text="✓" if tarea['completada'] else " ",
                                    selectcolor="#f0f0f0" if tarea['completada'] else "#e6f2ff")
            checkbox.grid(row=0, column=0, padx=(0, 5))
            
            # Estilo del título según estado
            estilo_titulo = {
                'text': tarea['titulo'],
                'anchor': "w",
                'relief': "flat",
                'cursor': "hand2"
            }
            
            if tarea['completada']:
                estilo_titulo.update({
                    'bg': '#f0f0f0',
                    'fg': 'gray'
                })
            else:
                estilo_titulo.update({
                    'bg': '#e6f2ff',
                    'fg': 'black'
                })
            
            # Botón con el título que muestra detalles
            boton_titulo = tk.Button(frame_tarea, **estilo_titulo,
                                   command=lambda t=tarea: mostrar_detalles_tarea(t))
            boton_titulo.grid(row=0, column=1, sticky="ew")
            
            # Botones de acción
            frame_botones = tk.Frame(frame_tarea)
            frame_botones.grid(row=0, column=2, padx=(5, 0))
            
            boton_editar = tk.Button(frame_botones, text="✏️", command=lambda idx=i: mostrar_formulario_editar(idx))
            boton_editar.pack(side=tk.LEFT, padx=2)
            
            boton_eliminar = tk.Button(frame_botones, text="🗑️", command=lambda idx=i: confirmar_eliminar(idx))
            boton_eliminar.pack(side=tk.LEFT, padx=2)
            
            # Configurar el grid para que el título ocupe el espacio disponible
            frame_tarea.grid_columnconfigure(1, weight=1)
    
    # Actualizar estadísticas después de actualizar la lista
    actualizar_estadisticas()

def salir():
    """Cierra la ventana de la aplicación."""
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Organizador de Tareas")
ventana.geometry("550x600")  # Aumentado el alto para acomodar el panel de estadísticas
ventana.configure(bg="#e6f2ff")

# Configurar el grid de la ventana principal para que sea expansible
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(3, weight=1)  # Cambiado a 3 para acomodar el panel de estadísticas

# Datos de las tareas cargados desde el archivo
tareas = cargar_tareas()

# Widgets
etiqueta_titulo_principal = tk.Label(ventana, text="Organizador de Tareas", font=("Arial", 18), bg="#e6f2ff")
etiqueta_titulo_principal.grid(row=0, column=0, pady=10)

# Frame para estadísticas
frame_estadisticas = tk.Frame(ventana, bg="#e6f2ff", relief="solid", bd=1)
frame_estadisticas.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

# Etiquetas para estadísticas
label_total = tk.Label(frame_estadisticas, text="Total de Tareas: 0", bg="#e6f2ff")
label_total.grid(row=0, column=0, padx=5, pady=2)

label_completadas = tk.Label(frame_estadisticas, text="Tareas Completadas: 0", bg="#e6f2ff")
label_completadas.grid(row=0, column=1, padx=5, pady=2)

label_pendientes = tk.Label(frame_estadisticas, text="Tareas Pendientes: 0", bg="#e6f2ff")
label_pendientes.grid(row=0, column=2, padx=5, pady=2)

label_porcentaje = tk.Label(frame_estadisticas, text="Porcentaje de Avance: 0%", bg="#e6f2ff")
label_porcentaje.grid(row=1, column=0, columnspan=3, padx=5, pady=2)

# Barra de progreso
barra_progreso = ttk.Progressbar(frame_estadisticas, length=300, mode='determinate')
barra_progreso.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

boton_agregar_tarea = tk.Button(ventana, text="Agregar Tarea", command=mostrar_formulario_agregar)
boton_agregar_tarea.grid(row=2, column=0, pady=10)

# Frame para contener la lista de tareas
frame_lista = tk.Frame(ventana)
frame_lista.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
frame_lista.grid_columnconfigure(0, weight=1)

# Inicializar la lista de tareas y estadísticas al iniciar la aplicación
actualizar_lista_tareas()

boton_salir = tk.Button(ventana, text="Salir", command=salir)
boton_salir.grid(row=4, column=0, pady=20)

# Iniciar aplicación
ventana.mainloop()