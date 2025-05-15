"""
Utilidades para la interfaz de usuario del Creador de Carteras Cripto HD.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import qrcode
from io import BytesIO
import base64
import webbrowser
import json
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

# Importar constantes de la interfaz de usuario
from .ui_constants import THEMES, LANGUAGES, FONT_SIZES, BUTTON_STYLES, \
    ENTRY_STYLES, LABEL_STYLES, FRAME_STYLES, NOTEBOOK_STYLES, \
    TREEVIEW_STYLES, SCROLLBAR_STYLES, MENU_STYLES, MESSAGE_STYLES

# Importar configuraciones
from config import Config

class ToolTip:
    """
    Crea un tooltip que aparece al pasar el ratón sobre un widget.
    """
    def __init__(self, widget: tk.Widget, text: str = '', bg: str = '#ffffe0',
                 fg: str = '#000000', delay: int = 250, **kwargs):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.delay = delay
        self.tooltip = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind('<Enter>', self.schedule)
        self.widget.bind('<Leave>', self.hide)
        self.widget.bind('<ButtonPress>', self.hide)

    def schedule(self, event: tk.Event = None) -> None:
        """Programa la aparición del tooltip."""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self) -> None:
        """Cancela la aparición programada del tooltip."""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show(self, event: tk.Event = None) -> None:
        """Muestra el tooltip."""
        if self.tooltip:
            return
            
        # Obtener la posición del ratón
        x, y, _, _ = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Crear la ventana del tooltip
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{x}+{y}')
        
        # Configurar el estilo del tooltip
        frame = ttk.Frame(
            self.tooltip,
            style='Tooltip.TFrame',
            borderwidth=1,
            relief='solid'
        )
        frame.pack()
        
        label = ttk.Label(
            frame,
            text=self.text,
            justify='left',
            background=self.bg,
            foreground=self.fg,
            relief='solid',
            borderwidth=0,
            padding=(4, 2)
        )
        label.pack()
        
        # Asegurarse de que el tooltip esté en primer plano
        self.tooltip.lift()
        self.tooltip.attributes('-topmost', True)
        
        # Actualizar el tooltip para asegurar que se muestre correctamente
        self.tooltip.update_idletasks()
        
        # Asegurarse de que el tooltip esté dentro de la pantalla
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        
        tooltip_width = self.tooltip.winfo_width()
        tooltip_height = self.tooltip.winfo_height()
        
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height - 10
            
        self.tooltip.wm_geometry(f'+{max(0, x)}+{max(0, y)}')

    def hide(self, event: tk.Event = None) -> None:
        """Oculta el tooltip."""
        self.unschedule()
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ValidatedEntry(ttk.Entry):
    """
    Entrada con validación personalizada.
    """
    def __init__(self, master=None, **kwargs):
        self.validate_cmd = kwargs.pop('validate', None)
        self.validate_on = kwargs.pop('validate_on', 'focusout')
        self.invalid_bg = kwargs.pop('invalid_bg', '#ffdddd')
        self.valid_bg = kwargs.pop('valid_bg', '#ffffff')
        self.default_bg = self.valid_bg
        
        # Configurar el estilo
        style = ttk.Style()
        style.configure('Valid.TEntry', fieldbackground=self.valid_bg)
        style.configure('Invalid.TEntry', fieldbackground=self.invalid_bg)
        
        # Llamar al constructor de la clase padre
        super().__init__(master, **kwargs)
        
        # Configurar la validación
        if self.validate_cmd is not None:
            if self.validate_on == 'key':
                self.validate_cmd = (self.register(self._on_validate), '%P')
                self.config(validate='key', validatecommand=self.validate_cmd)
            elif self.validate_on == 'focusout':
                self.bind('<FocusOut>', self._on_focus_out)
        
        # Configurar eventos
        self.bind('<FocusIn>', self._on_focus_in)
    
    def _on_validate(self, value: str) -> bool:
        """Valida el valor de entrada."""
        try:
            result = bool(self.validate_cmd(value))
            self._set_validation_style(result)
            return result
        except:
            self._set_validation_style(False)
            return False
    
    def _on_focus_out(self, event: tk.Event = None) -> None:
        """Maneja el evento de pérdida de foco."""
        if self.validate_cmd is not None:
            try:
                result = bool(self.validate_cmd(self.get()))
                self._set_validation_style(result)
            except:
                self._set_validation_style(False)
    
    def _on_focus_in(self, event: tk.Event = None) -> None:
        """Maneja el evento de obtención de foco."""
        self._set_validation_style(True)
    
    def _set_validation_style(self, is_valid: bool) -> None:
        """Establece el estilo según la validación."""
        if is_valid:
            self.config(style='Valid.TEntry')
        else:
            self.config(style='Invalid.TEntry')
    
    def validate(self) -> bool:
        """Valida el valor actual."""
        if self.validate_cmd is not None:
            try:
                result = bool(self.validate_cmd(self.get()))
                self._set_validation_style(result)
                return result
            except:
                self._set_validation_style(False)
                return False
        return True

class ScrolledFrame(ttk.Frame):
    """
    Marco con barras de desplazamiento.
    """
    def __init__(self, parent, *args, **kwargs):
        # Configurar el marco principal
        self.parent = parent
        self.canvas = tk.Canvas(parent, highlightthickness=0, **kwargs)
        self.scrollbar_v = ttk.Scrollbar(
            parent, 
            orient='vertical', 
            command=self.canvas.yview
        )
        self.scrollbar_h = ttk.Scrollbar(
            parent, 
            orient='horizontal', 
            command=self.canvas.xview
        )
        
        # Configurar el marco desplazable
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )
        
        # Crear una ventana en el canvas para el marco desplazable
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        # Configurar el desplazamiento del canvas
        self.canvas.configure(
            yscrollcommand=self.scrollbar_v.set,
            xscrollcommand=self.scrollbar_h.set
        )
        
        # Empaquetar los widgets
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.scrollbar_v.grid(row=0, column=1, sticky='ns')
        self.scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar el redimensionamiento
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Configurar el evento de redimensionamiento
        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Configurar el desplazamiento con la rueda del ratón
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.canvas.bind_all('<Shift-MouseWheel>', self._on_shift_mousewheel)
    
    def _on_frame_configure(self, event: tk.Event = None) -> None:
        """Actualiza la región de desplazamiento cuando cambia el tamaño del marco."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_canvas_configure(self, event: tk.Event = None) -> None:
        """Ajusta el tamaño del marco al cambiar el tamaño del canvas."""
        self.canvas.itemconfig('inner_frame', width=event.width)
    
    def _on_mousewheel(self, event: tk.Event) -> None:
        """Maneja el desplazamiento vertical con la rueda del ratón."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    
    def _on_shift_mousewheel(self, event: tk.Event) -> None:
        """Maneja el desplazamiento horizontal con Mayús + rueda del ratón."""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), 'units')
    
    def __getattr__(self, name: str) -> Any:
        """Redirige los atributos no encontrados al marco desplazable."""
        return getattr(self.scrollable_frame, name)

class QRCodeDialog(tk.Toplevel):
    """
    Diálogo para mostrar un código QR.
    """
    def __init__(self, parent, data: str, title: str = 'Código QR', **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        # Configurar la ventana
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
        # Generar el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Crear la imagen del código QR
        qr_image = qr.make_image(fill_color='black', back_color='white')
        
        # Convertir la imagen a un formato que Tkinter pueda mostrar
        self.qr_photo = ImageTk.PhotoImage(qr_image)
        
        # Mostrar la imagen
        qr_label = ttk.Label(self, image=self.qr_photo)
        qr_label.pack(padx=20, pady=20)
        
        # Mostrar los datos debajo del código QR
        data_label = ttk.Label(
            self, 
            text=data[:50] + '...' if len(data) > 50 else data,
            wraplength=300,
            justify='center'
        )
        data_label.pack(padx=20, pady=(0, 20))
        
        # Botón para copiar al portapapeles
        copy_btn = ttk.Button(
            self, 
            text='Copiar al portapapeles',
            command=lambda: self.copy_to_clipboard(data)
        )
        copy_btn.pack(pady=(0, 20))
        
        # Centrar la ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def copy_to_clipboard(self, text: str) -> None:
        """Copia el texto al portapapeles."""
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo(
            'Copiado', 
            'El texto ha sido copiado al portapapeles.',
            parent=self
        )
