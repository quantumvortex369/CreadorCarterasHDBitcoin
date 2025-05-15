"""
Módulo que contiene el diálogo de configuración de red.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, List, Tuple

# Importar utilidades de la interfaz de usuario
import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui_utils import ToolTip, ValidatedEntry, ScrolledFrame

def show_message(title, message, parent=None):
    """Muestra un mensaje de información."""
    try:
        if parent is None and hasattr(tk, '_default_root') and tk._default_root is not None:
            parent = tk._default_root
        return messagebox.showinfo(title, message, parent=parent)
    except Exception as e:
        print(f"Error al mostrar mensaje: {e}")
        return None

def show_info(message, parent=None):
    """Muestra un mensaje informativo."""
    return show_message("Información", message, parent)

def show_warning(message, parent=None):
    """Muestra un mensaje de advertencia."""
    try:
        if parent is None and hasattr(tk, '_default_root') and tk._default_root is not None:
            parent = tk._default_root
        return messagebox.showwarning("Advertencia", message, parent=parent)
    except Exception as e:
        print(f"Error al mostrar advertencia: {e}")
        return None

def show_error(message, parent=None):
    """Muestra un mensaje de error."""
    try:
        if parent is None and hasattr(tk, '_default_root') and tk._default_root is not None:
            parent = tk._default_root
        return messagebox.showerror("Error", message, parent=parent)
    except Exception as e:
        print(f"Error al mostrar error: {e}")
        return None

def ask_question(title, message, parent=None):
    """Hace una pregunta de sí/no al usuario."""
    try:
        if parent is None and hasattr(tk, '_default_root') and tk._default_root is not None:
            parent = tk._default_root
        return messagebox.askyesno(title, message, parent=parent)
    except Exception as e:
        print(f"Error al hacer pregunta: {e}")
        return False

def center_window(window, width=None, height=None):
    """Centra una ventana en la pantalla."""
    window.update_idletasks()
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_tooltip(widget, text):
    """Crea un tooltip para un widget."""
    return ToolTip(widget, text)

class NetworkSettingsDialog(tk.Toplevel):
    """Diálogo de configuración de red."""
    
    def __init__(self, parent, current_settings: Dict[str, Any], **kwargs):
        """Inicializa el diálogo de configuración de red.
        
        Args:
            parent: Ventana padre
            current_settings: Diccionario con la configuración actual de red
            **kwargs: Argumentos adicionales para el Toplevel
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_settings = current_settings.copy()
        self.result = None
        
        self.title("Configuración de Red")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Configurar el estilo
        self.style = ttk.Style()
        self._setup_styles()
        
        self._create_widgets()
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # Centrar el diálogo en la pantalla
        center_window(self, 500, 400)
    
    def _setup_styles(self):
        """Configura los estilos para el diálogo."""
        # Estilo para los botones
        self.style.configure(
            'Accent.TButton',
            font=('Arial', 10, 'bold'),
            padding=5
        )
    
    def _create_widgets(self):
        """Crea y configura los widgets del diálogo."""
        # Marco principal
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modo de conexión
        ttk.Label(
            main_frame,
            text="Modo de conexión:",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.mode_var = tk.StringVar(
            value=self.current_settings.get('mode', 'auto'))
        
        ttk.Radiobutton(
            main_frame,
            text="Automático (recomendado)",
            variable=self.mode_var,
            value='auto',
            command=self._update_ui_state
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=20, pady=2)
        
        ttk.Radiobutton(
            main_frame,
            text="Modo ligero (SPV) - Usa menos recursos",
            variable=self.mode_var,
            value='spv',
            command=self._update_ui_state
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=20, pady=2)
        
        ttk.Radiobutton(
            main_frame,
            text="Nodo completo - Mayor seguridad y privacidad",
            variable=self.mode_var,
            value='full',
            command=self._update_ui_state
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=20, pady=2)
        
        # Servidores personalizados
        ttk.Label(
            main_frame,
            text="Servidores personalizados:",
            font=('Arial', 10, 'bold')
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
        
        self.custom_servers_var = tk.BooleanVar(
            value=self.current_settings.get('use_custom_servers', False))
        
        self.custom_servers_cb = ttk.Checkbutton(
            main_frame,
            text="Usar servidores personalizados",
            variable=self.custom_servers_var,
            command=self._update_ui_state
        )
        self.custom_servers_cb.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=20, pady=2)
        
        # Frame para la lista de servidores
        servers_frame = ttk.LabelFrame(
            main_frame,
            text="Servidores",
            padding=5
        )
        servers_frame.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=5)
        
        # Lista de servidores
        self.servers_listbox = tk.Listbox(
            servers_frame,
            height=4,
            width=50,
            selectmode=tk.SINGLE
        )
        self.servers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de desplazamiento para la lista de servidores
        scrollbar = ttk.Scrollbar(servers_frame, orient=tk.VERTICAL, command=self.servers_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.servers_listbox.config(yscrollcommand=scrollbar.set)
        
        # Botones para gestionar servidores
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            buttons_frame,
            text="Agregar servidor...",
            command=self._on_add_server
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text="Editar",
            command=self._on_edit_server
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text="Eliminar",
            command=self._on_remove_server
        ).pack(side=tk.LEFT, padx=2)
        
        # Botones de acción
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(
            action_frame,
            text="Cancelar",
            command=self._on_cancel
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Aceptar",
            style='Accent.TButton',
            command=self._on_accept
        ).pack(side=tk.RIGHT, padx=5)
        
        # Cargar servidores existentes
        self._load_servers()
        
        # Actualizar estado inicial de la UI
        self._update_ui_state()
    
    def _load_servers(self):
        """Carga los servidores desde la configuración actual."""
        servers = self.current_settings.get('servers', [])
        for server in servers:
            self.servers_listbox.insert(tk.END, f"{server['host']}:{server['port']}")
    
    def _update_ui_state(self):
        """Actualiza el estado de los controles de la interfaz de usuario."""
        # Habilitar/deshabilitar controles según el modo seleccionado
        mode = self.mode_var.get()
        use_custom = self.custom_servers_var.get()
        
        # Si el modo es automático, deshabilitar la opción de servidores personalizados
        if mode == 'auto':
            self.custom_servers_cb.state(['disabled'])
            self.custom_servers_var.set(False)
            use_custom = False
        else:
            self.custom_servers_cb.state(['!disabled'])
        
        # Habilitar/deshabilitar controles de servidores según corresponda
        state = 'normal' if (mode != 'auto' and use_custom) else 'disabled'
        
        for widget in [self.servers_listbox]:
            widget.config(state=state)
    
    def _on_add_server(self):
        """Maneja el evento de agregar un nuevo servidor."""
        dialog = ServerDialog(self, title="Agregar Servidor")
        result = dialog.show()
        
        if result:
            host, port = result
            self.servers_listbox.insert(tk.END, f"{host}:{port}")
    
    def _on_edit_server(self):
        """Maneja el evento de editar un servidor existente."""
        selection = self.servers_listbox.curselection()
        if not selection:
            show_warning("Seleccione un servidor para editar.", parent=self)
            return
        
        index = selection[0]
        server_str = self.servers_listbox.get(index)
        host, port = server_str.split(':')
        
        dialog = ServerDialog(
            self,
            title="Editar Servidor",
            host=host,
            port=port
        )
        
        result = dialog.show()
        if result:
            new_host, new_port = result
            self.servers_listbox.delete(index)
            self.servers_listbox.insert(index, f"{new_host}:{new_port}")
    
    def _on_remove_server(self):
        """Maneja el evento de eliminar un servidor."""
        selection = self.servers_listbox.curselection()
        if not selection:
            show_warning("Seleccione un servidor para eliminar.", parent=self)
            return
        
        if ask_question(
            "Eliminar servidor",
            "¿Está seguro de que desea eliminar el servidor seleccionado?",
            parent=self
        ):
            for index in sorted(selection, reverse=True):
                self.servers_listbox.delete(index)
    
    def _on_accept(self):
        """Maneja el evento de clic en el botón Aceptar."""
        # Recopilar la configuración
        mode = self.mode_var.get()
        use_custom_servers = self.custom_servers_var.get()
        
        # Obtener la lista de servidores
        servers = []
        for i in range(self.servers_listbox.size()):
            server_str = self.servers_listbox.get(i)
            host, port = server_str.split(':')
            servers.append({
                'host': host,
                'port': int(port)
            })
        
        # Validar que haya al menos un servidor si se usa modo personalizado
        if use_custom_servers and not servers:
            show_error("Debe agregar al menos un servidor cuando usa servidores personalizados.", parent=self)
            return
        
        # Guardar la configuración
        self.result = {
            'mode': mode,
            'use_custom_servers': use_custom_servers,
            'servers': servers
        }
        
        self.destroy()
    
    def _on_cancel(self):
        """Maneja el evento de clic en el botón Cancelar."""
        self.result = None
        self.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Muestra el diálogo y devuelve el resultado.
        
        Returns:
            Dict[str, Any]: Diccionario con la configuración de red actualizada o None si se canceló
        """
        self.wait_window(self)
        return self.result


class ServerDialog(tk.Toplevel):
    """Diálogo para agregar/editar un servidor."""
    
    def __init__(self, parent, title: str, host: str = "", port: int = 8333, **kwargs):
        """Inicializa el diálogo de servidor.
        
        Args:
            parent: Ventana padre
            title: Título del diálogo
            host: Dirección del host del servidor
            port: Puerto del servidor
            **kwargs: Argumentos adicionales para el Toplevel
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        self.host = tk.StringVar(value=host)
        self.port = tk.StringVar(value=str(port))
        self.result = None
        
        self._create_widgets()
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # Centrar el diálogo en la pantalla
        center_window(self, 400, 200)
    
    def _create_widgets(self):
        """Crea y configura los widgets del diálogo."""
        # Marco principal
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo de host
        ttk.Label(main_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
        host_entry = ttk.Entry(main_frame, textvariable=self.host, width=30)
        host_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Campo de puerto
        ttk.Label(main_frame, text="Puerto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        port_entry = ttk.Entry(main_frame, textvariable=self.port, width=10)
        port_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self._on_cancel
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Aceptar",
            style='Accent.TButton',
            command=self._on_accept
        ).pack(side=tk.RIGHT, padx=5)
        
        # Configurar el peso de las columnas
        main_frame.columnconfigure(1, weight=1)
    
    def _on_accept(self):
        """Maneja el evento de clic en el botón Aceptar."""
        # Validar los datos
        host = self.host.get().strip()
        port_str = self.port.get().strip()
        
        if not host:
            show_error("Debe especificar un host.", parent=self)
            return
        
        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError("Puerto fuera de rango")
        except ValueError:
            show_error("El puerto debe ser un número entre 1 y 65535.", parent=self)
            return
        
        self.result = (host, port)
        self.destroy()
    
    def _on_cancel(self):
        """Maneja el evento de clic en el botón Cancelar."""
        self.result = None
        self.destroy()
    
    def show(self) -> Optional[tuple]:
        """Muestra el diálogo y devuelve el resultado.
        
        Returns:
            tuple: Tupla con (host, port) o None si se canceló
        """
        self.wait_window(self)
        return self.result
