"""
Módulo que contiene los diálogos de preferencias y configuración de la aplicación.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Any, Optional, List, Tuple
import os

# Importar utilidades de la interfaz de usuario
import os
import sys

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui_utils import ToolTip, ValidatedEntry, ScrolledFrame, QRCodeDialog
from utils.ui_constants import THEMES, LANGUAGES, BUTTON_STYLES

# Tamaños de fuente disponibles
FONT_SIZES = [
    ('Pequeño', 9),
    ('Mediano', 11),
    ('Grande', 13),
    ('Muy grande', 15)
]

FONT_SIZES_PX = {name: size for name, size in FONT_SIZES}

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

class PreferencesDialog(tk.Toplevel):
    """Diálogo de preferencias de la aplicación."""
    
    def __init__(self, parent, current_prefs: Dict[str, Any], **kwargs):
        """Inicializa el diálogo de preferencias.
        
        Args:
            parent: Ventana padre
            current_prefs: Diccionario con las preferencias actuales
            **kwargs: Argumentos adicionales para el Toplevel
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_prefs = current_prefs.copy()
        self.result = None
        
        self.title("Preferencias")
        self.geometry("700x600")
        self.minsize(600, 500)
        self.resizable(True, True)
        
        # Configurar el estilo
        self.style = ttk.Style()
        self._setup_styles()
        
        self._create_widgets()
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        # Centrar el diálogo en la pantalla
        center_window(self, 700, 600)
    
    def _setup_styles(self):
        """Configura los estilos para el diálogo."""
        # Estilo para los botones de pestaña
        self.style.configure(
            'Custom.TNotebook.Tab',
            padding=[10, 5],
            font=('Arial', 10, 'bold')
        )
        
        # Estilo para los botones
        self.style.configure(
            'Accent.TButton',
            font=('Arial', 10, 'bold'),
            padding=5
        )
    
    def _create_widgets(self):
        """Crea y configura los widgets del diálogo."""
        # Marco principal con notebook
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de interfaz
        self._create_interface_tab()
        
        # Pestaña de red
        self._create_network_tab()
        
        # Pestaña de monedas
        self._create_currencies_tab()
        
        # Pestaña de seguridad
        self._create_security_tab()
        
        # Pestaña de copias de seguridad
        self._create_backup_tab()
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Restaurar valores predeterminados",
            command=self._on_restore_defaults
        ).pack(side=tk.LEFT)
        
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
        ).pack(side=tk.RIGHT)
    
    def _create_interface_tab(self):
        """Crea la pestaña de configuración de la interfaz."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Interfaz")
        
        # Marco con scroll
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tema
        ttk.Label(
            scrollable_frame,
            text="Tema:",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.theme_var = tk.StringVar(value=self.current_prefs.get('ui.theme', 'light'))
        theme_frame = ttk.Frame(scrollable_frame)
        theme_frame.grid(row=1, column=0, sticky=tk.W, padx=20, pady=(0, 10))
        
        for i, (theme_id, theme_data) in enumerate(THEMES.items()):
            ttk.Radiobutton(
                theme_frame,
                text=theme_data['name'],
                variable=self.theme_var,
                value=theme_id
            ).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Idioma
        ttk.Label(
            scrollable_frame,
            text="Idioma:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.language_var = tk.StringVar(
            value=self.current_prefs.get('ui.language', 'es'))
        
        lang_frame = ttk.Frame(scrollable_frame)
        lang_frame.grid(row=3, column=0, sticky=tk.W, padx=20, pady=(0, 10))
        
        for i, (lang_code, lang_name) in enumerate(LANGUAGES.items()):
            ttk.Radiobutton(
                lang_frame,
                text=lang_name,
                variable=self.language_var,
                value=lang_code
            ).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Tamaño de fuente
        ttk.Label(
            scrollable_frame,
            text="Tamaño de fuente:",
            font=('Arial', 10, 'bold')
        ).grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        self.font_size_var = tk.StringVar(
            value=self.current_prefs.get('ui.font_size', 'normal'))
        
        font_frame = ttk.Frame(scrollable_frame)
        font_frame.grid(row=5, column=0, sticky=tk.W, padx=20, pady=(0, 10))
        
        for i, (size_key, size_name) in enumerate(FONT_SIZES_PX.items()):
            ttk.Radiobutton(
                font_frame,
                text=f"{size_name} ({FONT_SIZES[size_key]}px)",
                variable=self.font_size_var,
                value=size_key
            ).grid(row=i, column=0, sticky=tk.W, pady=2)
        
        # Actualizar el frame para que el scroll funcione correctamente
        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Configurar el scroll del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self._on_mousewheel = _on_mousewheel
    
    def _create_network_tab(self):
        """Crea la pestaña de configuración de red."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Red")
        
        # Configuración de nodo
        ttk.Label(
            tab,
            text="Configuración del Nodo",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Modo de conexión
        ttk.Label(tab, text="Modo de conexión:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.network_mode_var = tk.StringVar(
            value=self.current_prefs.get('network.mode', 'auto'))
        
        ttk.Combobox(
            tab,
            textvariable=self.network_mode_var,
            values=[
                'Automático (recomendado)',
                'Modo ligero (SPV)',
                'Nodo completo'
            ],
            state='readonly',
            width=30
        ).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Servidores personalizados
        ttk.Checkbutton(
            tab,
            text="Usar servidores personalizados",
            variable=tk.BooleanVar(value=self.current_prefs.get('network.custom_servers', False))
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        # Proxy
        ttk.Label(
            tab,
            text="Configuración de Proxy",
            font=('Arial', 10, 'bold')
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        # Configuración de proxy
        proxy_frame = ttk.LabelFrame(tab, text="Proxy")
        proxy_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5, ipadx=5, ipady=5)
        
        ttk.Checkbutton(
            proxy_frame,
            text="Usar proxy",
            variable=tk.BooleanVar(value=self.current_prefs.get('network.proxy.enabled', False))
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(proxy_frame, text="Tipo:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Combobox(
            proxy_frame,
            values=['SOCKS4', 'SOCKS5', 'HTTP'],
            state='readonly',
            width=10
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(proxy_frame, text="Servidor:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(proxy_frame, width=25).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(proxy_frame, text="Puerto:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(proxy_frame, width=10).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(proxy_frame, text="Usuario:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(proxy_frame, width=25).grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(proxy_frame, text="Contraseña:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(proxy_frame, width=25, show="*").grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Configurar el peso de las columnas
        tab.columnconfigure(1, weight=1)
    
    def _create_currencies_tab(self):
        """Crea la pestaña de configuración de monedas."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Monedas")
        
        # Moneda principal
        ttk.Label(
            tab,
            text="Moneda principal:",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        
        self.main_currency_var = tk.StringVar(
            value=self.current_prefs.get('currency.main', 'USD'))
        
        currencies = [
            ('USD', 'Dólar Estadounidense (USD)'),
            ('EUR', 'Euro (EUR)'),
            ('BTC', 'Bitcoin (BTC)'),
            ('SAT', 'Satoshi (SAT)'),
            ('GBP', 'Libra Esterlina (GBP)'),
            ('JPY', 'Yen Japonés (JPY)')
        ]
        
        ttk.Combobox(
            tab,
            textvariable=self.main_currency_var,
            values=[f"{code} - {name}" for code, name in currencies],
            state='readonly',
            width=30
        ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        
        # Monedas mostradas
        ttk.Label(
            tab,
            text="Monedas mostradas:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        
        # Lista de monedas disponibles
        currencies_frame = ttk.Frame(tab)
        currencies_frame.grid(row=3, column=0, sticky=tk.NSEW, padx=10, pady=5)
        
        # Lista de monedas seleccionadas
        self.selected_currencies = tk.Listbox(
            currencies_frame,
            selectmode=tk.MULTIPLE,
            height=8,
            width=30
        )
        
        # Agregar monedas a la lista
        for code, name in currencies:
            self.selected_currencies.insert(tk.END, f"{code} - {name}")
        
        self.selected_currencies.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botones para mover monedas
        buttons_frame = ttk.Frame(currencies_frame)
        buttons_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="↑",
            width=3,
            command=self._move_currency_up
        ).pack(pady=2)
        
        ttk.Button(
            buttons_frame,
            text="↓",
            width=3,
            command=self._move_currency_down
        ).pack(pady=2)
        
        # Configurar el peso de las columnas
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
    
    def _create_security_tab(self):
        """Crea la pestaña de configuración de seguridad."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Seguridad")
        
        # Configuración de contraseña
        ttk.Label(
            tab,
            text="Contraseña de la billetera",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Cambiar contraseña
        ttk.Button(
            tab,
            text="Cambiar contraseña",
            command=self._on_change_password
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        # Tiempo de bloqueo automático
        ttk.Label(
            tab,
            text="Bloqueo automático:",
            font=('Arial', 10, 'bold')
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        self.lock_timeout_var = tk.StringVar(
            value=str(self.current_prefs.get('security.lock_timeout', 15)))
        
        ttk.Combobox(
            tab,
            textvariable=self.lock_timeout_var,
            values=[
                '1 minuto',
                '5 minutos',
                '15 minutos',
                '30 minutos',
                '1 hora',
                'Nunca'
            ],
            state='readonly',
            width=15
        ).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        
        # Opciones de privacidad
        ttk.Label(
            tab,
            text="Opciones de privacidad",
            font=('Arial', 10, 'bold')
        ).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        self.privacy_options = {
            'obfuscate_amounts': tk.BooleanVar(
                value=self.current_prefs.get('privacy.obfuscate_amounts', False)),
            'hide_balances': tk.BooleanVar(
                value=self.current_prefs.get('privacy.hide_balances', False)),
            'hide_transaction_graphs': tk.BooleanVar(
                value=self.current_prefs.get('privacy.hide_transaction_graphs', False))
        }
        
        ttk.Checkbutton(
            tab,
            text="Ofuscar cantidades en la interfaz",
            variable=self.privacy_options['obfuscate_amounts']
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10, pady=2)
        
        ttk.Checkbutton(
            tab,
            text="Ocultar saldos por defecto",
            variable=self.privacy_options['hide_balances']
        ).grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=2)
        
        ttk.Checkbutton(
            tab,
            text="Ocultar gráficos de transacciones",
            variable=self.privacy_options['hide_transaction_graphs']
        ).grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=2)
        
        # Configurar el peso de las columnas
        tab.columnconfigure(1, weight=1)
    
    def _create_backup_tab(self):
        """Crea la pestaña de configuración de copias de seguridad."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Copia de Seguridad")
        
        # Configuración de copia de seguridad automática
        ttk.Label(
            tab,
            text="Copia de seguridad automática",
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.backup_enabled_var = tk.BooleanVar(
            value=self.current_prefs.get('backup.enabled', True))
        
        ttk.Checkbutton(
            tab,
            text="Habilitar copia de seguridad automática",
            variable=self.backup_enabled_var,
            command=self._toggle_backup_options
        ).grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        
        # Frecuencia de copia de seguridad
        ttk.Label(tab, text="Frecuencia:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.backup_freq_var = tk.StringVar(
            value=str(self.current_prefs.get('backup.frequency', '7')))
        
        ttk.Combobox(
            tab,
            textvariable=self.backup_freq_var,
            values=[
                'Diaria',
                'Semanal',
                'Mensual'
            ],
            state='readonly',
            width=15
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Directorio de copia de seguridad
        ttk.Label(tab, text="Ubicación:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.backup_dir_var = tk.StringVar(
            value=self.current_prefs.get('backup.directory', ''))
        
        ttk.Entry(
            tab,
            textvariable=self.backup_dir_var,
            width=40,
            state='readonly'
        ).grid(row=3, column=1, sticky=tk.EW, padx=(0, 5), pady=5)
        
        ttk.Button(
            tab,
            text="Examinar...",
            command=self._browse_backup_dir
        ).grid(row=3, column=2, sticky=tk.W, pady=5)
        
        # Última copia de seguridad
        ttk.Label(tab, text="Última copia:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        
        last_backup = self.current_prefs.get('backup.last_backup', 'Nunca')
        ttk.Label(tab, text=last_backup).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            button_frame,
            text="Realizar copia de seguridad ahora",
            command=self._on_backup_now
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Restaurar desde copia",
            command=self._on_restore_backup
        ).pack(side=tk.LEFT, padx=5)
        
        # Configurar el peso de las columnas
        tab.columnconfigure(1, weight=1)
    
    def _toggle_backup_options(self):
        """Habilita/deshabilita las opciones de copia de seguridad."""
        state = 'normal' if self.backup_enabled_var.get() else 'disabled'
        
        # No podemos acceder a los widgets directamente, necesitamos una referencia
        if hasattr(self, 'backup_widgets'):
            for widget in self.backup_widgets:
                widget.configure(state=state)
    
    def _browse_backup_dir(self):
        """Abre un diálogo para seleccionar el directorio de copia de seguridad."""
        directory = filedialog.askdirectory(
            title="Seleccionar directorio de copia de seguridad",
            mustexist=True
        )
        
        if directory:
            self.backup_dir_var.set(directory)
    
    def _on_backup_now(self):
        """Maneja el evento de realizar copia de seguridad ahora."""
        # Implementar lógica de copia de seguridad
        show_info("Copia de seguridad", "Se ha realizado una copia de seguridad de tus datos.")
    
    def _on_restore_backup(self):
        """Maneja el evento de restaurar desde copia de seguridad."""
        # Implementar lógica de restauración
        if ask_question("Restaurar copia de seguridad", 
                        "¿Está seguro de que desea restaurar desde una copia de seguridad?"):
            file = filedialog.askopenfilename(
                title="Seleccionar archivo de copia de seguridad",
                filetypes=[("Archivos de copia de seguridad", "*.bak"), ("Todos los archivos", "*.*")]
            )
            
            if file:
                show_info("Restauración", "La restauración se ha completado correctamente.")
    
    def _move_currency_up(self):
        """Mueve la moneda seleccionada hacia arriba en la lista."""
        selected = self.selected_currencies.curselection()
        if not selected or selected[0] == 0:
            return
        
        for pos in selected:
            if pos > 0:
                text = self.selected_currencies.get(pos)
                self.selected_currencies.delete(pos)
                self.selected_currencies.insert(pos - 1, text)
                self.selected_currencies.selection_set(pos - 1)
    
    def _move_currency_down(self):
        """Mueve la moneda seleccionada hacia abajo en la lista."""
        selected = self.selected_currencies.curselection()
        if not selected or selected[-1] == self.selected_currencies.size() - 1:
            return
        
        for pos in reversed(selected):
            if pos < self.selected_currencies.size() - 1:
                text = self.selected_currencies.get(pos)
                self.selected_currencies.delete(pos)
                self.selected_currencies.insert(pos + 1, text)
                self.selected_currencies.selection_set(pos + 1)
    
    def _on_change_password(self):
        """Maneja el evento de cambio de contraseña."""
        dialog = PasswordDialog(
            self,
            title="Cambiar contraseña",
            message="Ingrese la nueva contraseña para la billetera:",
            confirm=True
        )
        
        result = dialog.show()
        if result:
            # Aquí iría la lógica para cambiar la contraseña
            show_info("Contraseña cambiada", "La contraseña se ha cambiado correctamente.")
    
    def _on_restore_defaults(self):
        """Restaura los valores predeterminados."""
        if ask_question(
            "Restaurar valores predeterminados",
            "¿Está seguro de que desea restaurar todos los valores predeterminados?\n\n"
            "Se perderán todos los cambios no guardados.",
            parent=self
        ):
            # Aquí iría la lógica para restaurar los valores predeterminados
            show_info("Valores restaurados", "Se han restaurado los valores predeterminados.")
    
    def _on_accept(self):
        """Maneja el evento de clic en el botón Aceptar."""
        # Recopilar todas las preferencias
        prefs = {
            'ui.theme': self.theme_var.get(),
            'ui.language': self.language_var.get(),
            'ui.font_size': self.font_size_var.get(),
            'network.mode': self.network_mode_var.get(),
            'currency.main': self.main_currency_var.get().split(' ')[0],
            'security.lock_timeout': int(self.lock_timeout_var.get().split(' ')[0]) if self.lock_timeout_var.get() != 'Nunca' else 0,
            'privacy.obfuscate_amounts': self.privacy_options['obfuscate_amounts'].get(),
            'privacy.hide_balances': self.privacy_options['hide_balances'].get(),
            'privacy.hide_transaction_graphs': self.privacy_options['hide_transaction_graphs'].get(),
            'backup.enabled': self.backup_enabled_var.get(),
            'backup.frequency': {'Diaria': 1, 'Semanal': 7, 'Mensual': 30}[self.backup_freq_var.get()],
            'backup.directory': self.backup_dir_var.get()
        }
        
        self.result = prefs
        self.destroy()
    
    def _on_cancel(self):
        """Maneja el evento de clic en el botón Cancelar."""
        self.result = None
        self.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Muestra el diálogo y devuelve el resultado.
        
        Returns:
            Dict[str, Any]: Diccionario con las preferencias actualizadas o None si se canceló
        """
        self.wait_window(self)
        return self.result

# La clase NetworkSettingsDialog se moverá a un archivo separado para mantener el código organizado
