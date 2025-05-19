import tkinter as tk
from tkinter import messagebox
import json
import os

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

def validar_tarea(titulo, descripcion=""):
    """Valida el título y la descripción de la tarea."""
    if not titulo.strip():
        messagebox.showwarning("Advertencia", "El título es obligatorio.")
        return False
    if len(titulo) > 50:
        messagebox.showwarning("Advertencia", "Máximo 50 caracteres para el título.")
        return False
    if len(titulo) < 1:
        messagebox.showwarning("Advertencia", "Mínimo 1 carácter para el título.")
        return False
    if len(descripcion) > 200:
        messagebox.showwarning("Advertencia", "Máximo 200 caracteres para la descripción.")
        return False
    return True

def mostrar_formulario_agregar():
    """Muestra el formulario para agregar una nueva tarea."""
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Agregar Nueva Tarea")
    dialogo.geometry("400x300")  # Tamaño inicial del diálogo
    
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
        titulo = entrada_titulo.get()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        if validar_tarea(titulo, descripcion):
            nueva_tarea = {"titulo": titulo, "descripcion": descripcion}
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
    dialogo.grab_set()  # Hace que la ventana sea modal
    ventana.wait_window(dialogo)

def confirmar_eliminar(indice):
    """Muestra un diálogo de confirmación antes de eliminar una tarea (solo Sí/No)."""
    tarea = tareas[indice]
    respuesta = messagebox.askyesno("Confirmar",
                                     f"¿Eliminar esta tarea?\n\"{tarea['titulo']}\"\nEsta acción no se puede deshacer.")
    if respuesta == True:
        del tareas[indice]
        guardar_tareas(tareas)
        actualizar_lista_tareas()
        # Opcional: messagebox.showinfo("Información", "Tarea eliminada correctamente.")

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
    
    # Título
    etiqueta_titulo = tk.Label(frame_contenido, text="Título:", font=("Arial", 10, "bold"))
    etiqueta_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    texto_titulo = tk.Label(frame_contenido, text=tarea['titulo'], wraplength=300)
    texto_titulo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    # Descripción
    etiqueta_descripcion = tk.Label(frame_contenido, text="Descripción:", font=("Arial", 10, "bold"))
    etiqueta_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    texto_descripcion = tk.Label(frame_contenido, text=tarea['descripcion'], wraplength=300)
    texto_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # Botón cerrar
    boton_cerrar = tk.Button(dialogo, text="Cerrar", command=dialogo.destroy)
    boton_cerrar.grid(row=2, column=0, pady=10)
    
    dialogo.transient(ventana)
    dialogo.grab_set()
    ventana.wait_window(dialogo)

def actualizar_lista_tareas():
    """Actualiza la visualización de la lista de tareas mostrando título y descripción."""
    for widget in frame_lista.winfo_children():
        widget.destroy()

    for i, tarea in enumerate(tareas):
        frame_tarea = tk.Frame(frame_lista)
        frame_tarea.pack(fill=tk.X, padx=5, pady=2)

        # Crear un botón con el título que al hacer clic muestre los detalles
        boton_titulo = tk.Button(frame_tarea, 
                               text=tarea['titulo'],
                               anchor="w",
                               relief="flat",
                               bg="#e6f2ff",
                               cursor="hand2",
                               command=lambda t=tarea: mostrar_detalles_tarea(t))
        boton_titulo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        boton_eliminar = tk.Button(frame_tarea, text="🗑️",
                                    command=lambda idx=i: confirmar_eliminar(idx))
        boton_eliminar.pack(side=tk.RIGHT)

def salir():
    """Cierra la ventana de la aplicación."""
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Organizador de Tareas")
ventana.geometry("550x500")
ventana.configure(bg="#e6f2ff")

# Configurar el grid de la ventana principal para que sea expansible
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_rowconfigure(2, weight=1)

# Datos de las tareas cargados desde el archivo
tareas = cargar_tareas()

# Widgets
etiqueta_titulo_principal = tk.Label(ventana, text="Organizador de Tareas", font=("Arial", 18), bg="#e6f2ff")
etiqueta_titulo_principal.grid(row=0, column=0, pady=10)

boton_agregar_tarea = tk.Button(ventana, text="Agregar Tarea", command=mostrar_formulario_agregar)
boton_agregar_tarea.grid(row=1, column=0, pady=10)

# Frame para contener la lista de tareas
frame_lista = tk.Frame(ventana)
frame_lista.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
frame_lista.grid_columnconfigure(0, weight=1)

# Inicializar la lista de tareas al iniciar la aplicación
actualizar_lista_tareas()

boton_salir = tk.Button(ventana, text="Salir", command=salir)
boton_salir.grid(row=3, column=0, pady=20)

# Iniciar aplicación
ventana.mainloop()