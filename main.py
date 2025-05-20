import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re
from datetime import datetime

# Nombre del archivo para guardar las tareas
ARCHIVO_TAREAS = "tareas.json"

# Constantes para categorías
CATEGORIAS = ["General", "Personal", "Trabajo", "Estudio"]
COLORES_CATEGORIAS = {
    "General": "#808080",  # Gris
    "Personal": "#4CAF50",  # Verde
    "Trabajo": "#2196F3",  # Azul
    "Estudio": "#FFC107"   # Amarillo
}

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

def crear_selector_fecha(parent):
    """Crea un frame con campos para seleccionar día, mes y año."""
    frame = tk.Frame(parent)
    
    # Listas de opciones
    dias = [str(i).zfill(2) for i in range(1, 32)]
    meses = [str(i).zfill(2) for i in range(1, 13)]
    anios = [str(i) for i in range(datetime.now().year, datetime.now().year + 10)]
    
    # Comboboxes
    combo_dia = ttk.Combobox(frame, values=dias, width=3, state="readonly")
    combo_mes = ttk.Combobox(frame, values=meses, width=3, state="readonly")
    combo_anio = ttk.Combobox(frame, values=anios, width=5, state="readonly")
    
    # Establecer valores actuales
    hoy = datetime.now()
    combo_dia.set(str(hoy.day).zfill(2))
    combo_mes.set(str(hoy.month).zfill(2))
    combo_anio.set(str(hoy.year))
    
    # Layout
    combo_dia.pack(side=tk.LEFT, padx=2)
    tk.Label(frame, text="/").pack(side=tk.LEFT)
    combo_mes.pack(side=tk.LEFT, padx=2)
    tk.Label(frame, text="/").pack(side=tk.LEFT)
    combo_anio.pack(side=tk.LEFT, padx=2)
    
    return frame, combo_dia, combo_mes, combo_anio

def mostrar_formulario_agregar():
    """Muestra el formulario para agregar una nueva tarea."""
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Agregar Nueva Tarea")
    dialogo.geometry("400x400")
    
    # Configurar el grid para que sea expansible
    dialogo.grid_columnconfigure(1, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    
    # Frame principal para el contenido
    frame_contenido = tk.Frame(dialogo)
    frame_contenido.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    frame_contenido.grid_columnconfigure(1, weight=1)
    
    # Campos del formulario
    etiqueta_titulo = tk.Label(frame_contenido, text="Título:")
    etiqueta_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entrada_titulo = tk.Entry(frame_contenido)
    entrada_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    etiqueta_descripcion = tk.Label(frame_contenido, text="Descripción:")
    etiqueta_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entrada_descripcion = tk.Text(frame_contenido, height=5)
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    # Campo de categoría
    etiqueta_categoria = tk.Label(frame_contenido, text="Categoría:")
    etiqueta_categoria.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    combo_categoria = ttk.Combobox(frame_contenido, values=CATEGORIAS, state="readonly")
    combo_categoria.set("General")
    combo_categoria.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    # Campo de fecha de vencimiento
    etiqueta_fecha = tk.Label(frame_contenido, text="Fecha de vencimiento:")
    etiqueta_fecha.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    frame_fecha, combo_dia, combo_mes, combo_anio = crear_selector_fecha(frame_contenido)
    frame_fecha.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    # Frame para los botones
    frame_botones = tk.Frame(dialogo)
    frame_botones.grid(row=1, column=0, columnspan=2, pady=10, sticky="s")
    
    def guardar_nueva_tarea():
        titulo = entrada_titulo.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        categoria = combo_categoria.get()
        fecha = f"{combo_dia.get()}/{combo_mes.get()}/{combo_anio.get()}"
        
        if validar_tarea(titulo, descripcion):
            nueva_tarea = {
                "titulo": titulo,
                "descripcion": descripcion,
                "completada": False,
                "categoria": categoria,
                "fecha_vencimiento": fecha,
                "importante": False
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
    dialogo.geometry("400x400")
    
    # Configurar el grid para que sea expansible
    dialogo.grid_columnconfigure(1, weight=1)
    dialogo.grid_rowconfigure(1, weight=1)
    
    # Frame principal para el contenido
    frame_contenido = tk.Frame(dialogo)
    frame_contenido.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    frame_contenido.grid_columnconfigure(1, weight=1)
    
    # Campos del formulario
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
    
    # Campo de categoría
    etiqueta_categoria = tk.Label(frame_contenido, text="Categoría:")
    etiqueta_categoria.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    combo_categoria = ttk.Combobox(frame_contenido, values=CATEGORIAS, state="readonly")
    combo_categoria.set(tarea.get('categoria', 'General'))
    combo_categoria.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    
    # Campo de fecha de vencimiento
    etiqueta_fecha = tk.Label(frame_contenido, text="Fecha de vencimiento:")
    etiqueta_fecha.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    frame_fecha, combo_dia, combo_mes, combo_anio = crear_selector_fecha(frame_contenido)
    frame_fecha.grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    # Establecer fecha actual si existe
    if 'fecha_vencimiento' in tarea:
        try:
            dia, mes, anio = tarea['fecha_vencimiento'].split('/')
            combo_dia.set(dia)
            combo_mes.set(mes)
            combo_anio.set(anio)
        except ValueError:
            pass
    
    # Frame para los botones
    frame_botones = tk.Frame(dialogo)
    frame_botones.grid(row=1, column=0, columnspan=2, pady=10, sticky="s")
    
    def actualizar_tarea():
        titulo = entrada_titulo.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        categoria = combo_categoria.get()
        fecha = f"{combo_dia.get()}/{combo_mes.get()}/{combo_anio.get()}"
        
        if validar_tarea(titulo, descripcion):
            tareas[indice].update({
                'titulo': titulo,
                'descripcion': descripcion,
                'categoria': categoria,
                'fecha_vencimiento': fecha
            })
            guardar_tareas(tareas)
            actualizar_lista_tareas()
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

def es_tarea_vencida(tarea):
    """Determina si una tarea está vencida."""
    if not tarea.get('fecha_vencimiento'):
        return False
    try:
        fecha_vencimiento = datetime.strptime(tarea['fecha_vencimiento'], "%d/%m/%Y")
        return datetime.now() > fecha_vencimiento and not tarea['completada']
    except ValueError:
        return False

def toggle_importante(indice):
    """Alterna el estado de importante de una tarea."""
    tareas[indice]['importante'] = not tareas[indice].get('importante', False)
    guardar_tareas(tareas)
    actualizar_lista_tareas()

def vaciar_lista():
    """Vacía la lista de tareas después de confirmación."""
    if not tareas:
        messagebox.showinfo("Información", "La lista ya está vacía.")
        return
        
    respuesta = messagebox.askyesno("Confirmar",
                                  "¿Estás seguro de que deseas eliminar todas las tareas?\nEsta acción no se puede deshacer.")
    if respuesta:
        tareas.clear()
        guardar_tareas(tareas)
        actualizar_lista_tareas()
        messagebox.showinfo("Información", "Lista vaciada correctamente.")

def actualizar_lista_tareas():
    """Actualiza la visualización de la lista de tareas."""
    for widget in frame_lista.winfo_children():
        widget.destroy()

    if not tareas:
        label_vacio = tk.Label(frame_lista, text="No hay tareas creadas.", fg="gray")
        label_vacio.pack(pady=10)
    else:
        # Ordenar tareas: primero las importantes, luego las vencidas, luego el resto
        tareas_ordenadas = sorted(tareas, 
                                key=lambda x: (
                                    not x.get('importante', False),  # Importantes primero
                                    not es_tarea_vencida(x),        # Vencidas después
                                    x.get('fecha_vencimiento', '')  # Por fecha
                                ))
        
        for i, tarea in enumerate(tareas_ordenadas):
            frame_tarea = tk.Frame(frame_lista)
            frame_tarea.pack(fill=tk.X, padx=5, pady=2)
            
            # Estilo base según estado
            estilo_base = {
                'bg': '#f0f0f0' if tarea['completada'] else '#e6f2ff',
                'fg': 'gray' if tarea['completada'] else 'black'
            }
            
            # Ajustar estilo si está vencida
            if es_tarea_vencida(tarea):
                estilo_base.update({'fg': 'red'})
            
            # Checkbox para estado completado
            var_check = tk.BooleanVar(value=tarea['completada'])
            checkbox = tk.Checkbutton(frame_tarea, 
                                    variable=var_check,
                                    command=lambda idx=i: toggle_completada(idx),
                                    indicatoron=False,
                                    width=2,
                                    text="✓" if tarea['completada'] else " ",
                                    selectcolor="#f0f0f0" if tarea['completada'] else "#e6f2ff")
            checkbox.grid(row=0, column=0, padx=(0, 5))
            
            # Ícono de estrella para importante
            var_importante = tk.BooleanVar(value=tarea.get('importante', False))
            boton_importante = tk.Checkbutton(frame_tarea,
                                            variable=var_importante,
                                            command=lambda idx=i: toggle_importante(idx),
                                            indicatoron=False,
                                            width=2,
                                            text="★" if tarea.get('importante', False) else "☆",
                                            fg="gold" if tarea.get('importante', False) else "gray")
            boton_importante.grid(row=0, column=1, padx=(0, 5))
            
            # Frame para título y fecha
            frame_info = tk.Frame(frame_tarea, bg=estilo_base['bg'])
            frame_info.grid(row=0, column=2, sticky="ew")
            
            # Título con categoría
            categoria = tarea.get('categoria', 'General')
            color_categoria = COLORES_CATEGORIAS.get(categoria, "#808080")
            
            etiqueta_categoria = tk.Label(frame_info, 
                                        text=f" [{categoria}] ",
                                        bg=color_categoria,
                                        fg="white",
                                        font=("Arial", 8))
            etiqueta_categoria.pack(side=tk.LEFT, padx=(0, 5))
            
            boton_titulo = tk.Button(frame_info,
                                   text=tarea['titulo'],
                                   anchor="w",
                                   relief="flat",
                                   cursor="hand2",
                                   bg=estilo_base['bg'],
                                   fg=estilo_base['fg'],
                                   command=lambda t=tarea: mostrar_detalles_tarea(t))
            boton_titulo.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Fecha de vencimiento
            if 'fecha_vencimiento' in tarea:
                color_fecha = 'red' if es_tarea_vencida(tarea) else 'gray'
                etiqueta_fecha = tk.Label(frame_info,
                                        text=f"Vence: {tarea['fecha_vencimiento']}",
                                        fg=color_fecha,
                                        bg=estilo_base['bg'],
                                        font=("Arial", 8))
                etiqueta_fecha.pack(side=tk.RIGHT, padx=5)
            
            # Botones de acción
            frame_botones = tk.Frame(frame_tarea)
            frame_botones.grid(row=0, column=3, padx=(5, 0))
            
            boton_editar = tk.Button(frame_botones, text="✏️", command=lambda idx=i: mostrar_formulario_editar(idx))
            boton_editar.pack(side=tk.LEFT, padx=2)
            
            boton_eliminar = tk.Button(frame_botones, text="🗑️", command=lambda idx=i: confirmar_eliminar(idx))
            boton_eliminar.pack(side=tk.LEFT, padx=2)
            
            # Configurar el grid para que el título ocupe el espacio disponible
            frame_tarea.grid_columnconfigure(2, weight=1)
    
    # Actualizar estadísticas después de actualizar la lista
    actualizar_estadisticas()

def salir():
    """Cierra la ventana de la aplicación."""
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Organizador de Tareas")
ventana.geometry("600x600")
ventana.configure(bg="#e6f2ff")

# Configurar el grid de la ventana principal
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(3, weight=1)

# Datos de las tareas
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

# Frame para botones superiores
frame_botones_superiores = tk.Frame(ventana, bg="#e6f2ff")
frame_botones_superiores.grid(row=2, column=0, pady=5)

boton_agregar_tarea = tk.Button(frame_botones_superiores, text="Agregar Tarea", command=mostrar_formulario_agregar)
boton_agregar_tarea.pack(side=tk.LEFT, padx=5)

boton_vaciar = tk.Button(frame_botones_superiores, text="Vaciar Lista", command=vaciar_lista, fg="red")
boton_vaciar.pack(side=tk.LEFT, padx=5)

# Frame para contener la lista de tareas
frame_lista = tk.Frame(ventana)
frame_lista.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")
frame_lista.grid_columnconfigure(0, weight=1)

# Inicializar la lista de tareas y estadísticas
actualizar_lista_tareas()

boton_salir = tk.Button(ventana, text="Salir", command=salir)
boton_salir.grid(row=4, column=0, pady=20)

# Iniciar aplicación
ventana.mainloop()