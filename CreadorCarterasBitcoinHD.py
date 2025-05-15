# -*- coding: utf-8 -*-
"""
Creador de Carteras Bitcoin HD
============================

Aplicación para generar y gestionar carteras Bitcoin HD (BIP-32/39/44)
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from datetime import datetime
import webbrowser
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import base64
import hashlib
import hmac
import ecdsa
import bech32
import unicodedata
import secrets
import string

# Añadir el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar dependencias de criptomonedas
try:
    from mnemonic import Mnemonic
    from bip32utils import BIP32Key
    from bitcoinutils.setup import setup
    from bitcoinutils.keys import P2pkhAddress, P2shAddress, P2wpkhAddress, PrivateKey, PublicKey
    from bitcoinutils.script import Script
except ImportError as e:
    print(f"Error al importar dependencias de criptomonedas: {e}")
    print("Por favor, instale las dependencias necesarias con: pip install -r requirements.txt")
    sys.exit(1)

# Importar diálogos
try:
    from dialogs.preferences_ui import PreferencesDialog
    from dialogs.network_settings_dialog import NetworkSettingsDialog
except ImportError as e:
    print(f"Error al importar diálogos: {e}")
    sys.exit(1)

# Importar utilidades
try:
    from utils.ui_utils import ToolTip, ValidatedEntry, ScrolledFrame, QRCodeDialog
    from utils.ui_constants import THEMES, LANGUAGES, BUTTON_STYLES
except ImportError as e:
    print(f"Error al importar utilidades: {e}")
    sys.exit(1)


# Constantes para tipos de direcciones
ADDR_TYPE_P2PKH = 'p2pkh'        # Legacy (1...)
ADDR_TYPE_P2SH_P2WPKH = 'p2sh'  # Nested SegWit (3...)
ADDR_TYPE_P2WPKH = 'p2wpkh'      # Native SegWit (bc1...)


class CreadorCarterasApp(tk.Tk):
    """Clase principal de la aplicación para crear carteras Bitcoin HD."""
    
    def __init__(self):
        """Inicializa la aplicación."""
        super().__init__()
        
        # Configuración básica de la ventana
        self.title("Creador de Carteras Bitcoin HD")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Configurar el tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar el icono de la aplicación
        try:
            self.iconbitmap(os.path.join('assets', 'icons', 'bitcoin.ico'))
        except:
            pass  # Si no se encuentra el icono, se usa el predeterminado
        
        # Inicializar variables
        self.semilla = None
        self.direcciones = []
        self.tipo_direccion = ADDR_TYPE_P2WPKH  # Por defecto, usar SegWit nativo
        
        # Configurar la interfaz
        self._configurar_interfaz()
        
        # Configurar el menú
        self._configurar_menu()
    
    def _configurar_interfaz(self):
        """Configura los elementos de la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sección de semilla
        seed_frame = ttk.LabelFrame(main_frame, text="Semilla Mnemotécnica", padding="5")
        seed_frame.pack(fill=tk.X, pady=5)
        
        self.seed_text = scrolledtext.ScrolledText(seed_frame, height=3, wrap=tk.WORD)
        self.seed_text.pack(fill=tk.X, expand=True)
        
        btn_frame = ttk.Frame(seed_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Generar Nueva Semilla", command=self._generar_semilla).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Importar Semilla", command=self._importar_semilla).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Copiar Semilla", command=self._copiar_semilla).pack(side=tk.LEFT, padx=2)
        
        # Sección de tipo de dirección
        addr_frame = ttk.LabelFrame(main_frame, text="Tipo de Dirección", padding="5")
        addr_frame.pack(fill=tk.X, pady=5)
        
        self.addr_type = tk.StringVar(value=ADDR_TYPE_P2WPKH)
        
        ttk.Radiobutton(addr_frame, text="SegWit Nativo (bc1...)", 
                       variable=self.addr_type, value=ADDR_TYPE_P2WPKH).pack(anchor=tk.W)
        ttk.Radiobutton(addr_frame, text="Nested SegWit (3...)", 
                       variable=self.addr_type, value=ADDR_TYPE_P2SH_P2WPKH).pack(anchor=tk.W)
        ttk.Radiobutton(addr_frame, text="Legacy (1...)", 
                       variable=self.addr_type, value=ADDR_TYPE_P2PKH).pack(anchor=tk.W)
        
        # Sección de generación de direcciones
        gen_frame = ttk.LabelFrame(main_frame, text="Generar Direcciones", padding="5")
        gen_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gen_frame, text="Número de direcciones a generar:").pack(side=tk.LEFT, padx=5)
        self.num_direcciones = ttk.Spinbox(gen_frame, from_=1, to=100, width=5)
        self.num_direcciones.pack(side=tk.LEFT, padx=5)
        self.num_direcciones.set("10")
        
        ttk.Button(gen_frame, text="Generar Direcciones", 
                  command=self._generar_direcciones).pack(side=tk.LEFT, padx=5)
        
        # Área de visualización de direcciones
        self.direcciones_frame = ttk.LabelFrame(main_frame, text="Direcciones Generadas", padding="5")
        self.direcciones_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Crear Treeview para mostrar direcciones
        columns = ("#", "Dirección", "Clave Privada (WIF)", "Saldo")
        self.tree = ttk.Treeview(self.direcciones_frame, columns=columns, show="headings", selectmode="browse")
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)
        
        # Ajustar ancho de columnas
        self.tree.column("#", width=50)
        self.tree.column("Dirección", width=300)
        self.tree.column("Clave Privada (WIF)", width=300)
        self.tree.column("Saldo", width=100)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.direcciones_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar Treeview y scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Menú contextual para copiar direcciones
        self._setup_context_menu()
    
    def _configurar_menu(self):
        """Configura la barra de menú de la aplicación."""
        menubar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nueva Cartera", command=self._nueva_cartera)
        file_menu.add_command(label="Abrir Cartera...", command=self._abrir_cartera)
        file_menu.add_command(label="Guardar Cartera Como...", command=self._guardar_cartera_como)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Preferencias", command=self._mostrar_preferencias)
        tools_menu.add_command(label="Configuración de Red", command=self._configurar_red)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentación", command=self._mostrar_documentacion)
        help_menu.add_command(label="Acerca de...", command=self._mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.config(menu=menubar)
    
    def _setup_context_menu(self):
        """Configura el menú contextual para la lista de direcciones."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copiar Dirección", command=self._copiar_direccion)
        self.context_menu.add_command(label="Copiar Clave Privada", command=self._copiar_clave_privada)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Ver en Explorador", command=self._ver_en_explorador)
        
        # Vincular evento de clic derecho
        self.tree.bind("<Button-3>", self._mostrar_menu_contextual)
    
    def _mostrar_menu_contextual(self, event):
        """Muestra el menú contextual en la posición del ratón."""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _generar_semilla(self):
        """Genera una nueva semilla mnemotécnica."""
        try:
            mnemo = Mnemonic("spanish")
            self.semilla = mnemo.generate(strength=256)  # 24 palabras
            self.seed_text.delete(1.0, tk.END)
            self.seed_text.insert(tk.END, self.semilla)
            self.direcciones = []  # Limpiar direcciones anteriores
            self._limpiar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar semilla: {str(e)}")
    
    def _importar_semilla(self):
        """Importa una semilla mnemotécnica existente."""
        semilla = self.seed_text.get(1.0, tk.END).strip()
        if not semilla:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una semilla mnemotécnica.")
            return
        
        try:
            # Validar la semilla
            mnemo = Mnemonic("spanish")
            if not mnemo.check(semilla):
                raise ValueError("Semilla mnemotécnica inválida")
                
            self.semilla = semilla
            self.direcciones = []  # Limpiar direcciones anteriores
            self._limpiar_tabla()
            messagebox.showinfo("Éxito", "Semilla importada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar semilla: {str(e)}")
    
    def _copiar_semilla(self):
        """Copia la semilla al portapapeles."""
        if not self.semilla:
            messagebox.showwarning("Advertencia", "No hay ninguna semilla para copiar.")
            return
            
        self.clipboard_clear()
        self.clipboard_append(self.semilla)
        messagebox.showinfo("Copiado", "La semilla ha sido copiada al portapapeles.")
    
    def _generar_direcciones(self):
        """Genera direcciones a partir de la semilla."""
        if not self.semilla:
            messagebox.showwarning("Advertencia", "Por favor, genere o importe una semilla primero.")
            return
        
        try:
            num_direcciones = int(self.num_direcciones.get())
            if num_direcciones < 1 or num_direcciones > 100:
                raise ValueError("El número de direcciones debe estar entre 1 y 100")
                
            # Limpiar direcciones anteriores
            self.direcciones = []
            self._limpiar_tabla()
            
            # Generar direcciones
            for i in range(num_direcciones):
                direccion = self._generar_direccion(i)
                self.direcciones.append(direccion)
                self._agregar_direccion_a_tabla(i, direccion)
                
            messagebox.showinfo("Éxito", f"Se han generado {num_direcciones} direcciones.")
            
        except ValueError as ve:
            messagebox.showerror("Error", f"Número de direcciones inválido: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar direcciones: {str(e)}")
    
    def _generar_direccion(self, indice):
        """
        Genera una dirección Bitcoin a partir de la semilla y el índice.
        
        Args:
            indice: Índice de la dirección a generar.
            
        Returns:
            dict: Diccionario con la información de la dirección generada.
        """
        try:
            # Configurar la red (mainnet o testnet)
            setup('mainnet')
            
            # Obtener la semilla como bytes
            mnemo = Mnemonic("spanish")
            seed_bytes = mnemo.to_seed(self.semilla)
            
            # Crear clave raíz BIP32
            root_key = BIP32Key.fromEntropy(seed_bytes)
            
            # Derivar según BIP44: m/44'/0'/0'/0/indice
            # 44' - Propósito (BIP44)
            # 0' - Moneda (Bitcoin)
            # 0' - Cuenta
            # 0 - Recepción/Cambio (0 para recepción)
            # indice - Índice de la dirección
            child_key = root_key.ChildKey(44 + 0x80000000)  # 44' (BIP44)
            child_key = child_key.ChildKey(0 + 0x80000000)   # 0' (Bitcoin)
            child_key = child_key.ChildKey(0 + 0x80000000)   # 0' (Cuenta)
            child_key = child_key.ChildKey(0)                # 0 (Recepción)
            child_key = child_key.ChildKey(indice)           # Índice
            
            # Obtener la clave privada en formato WIF
            wif = child_key.WalletImportFormat()
            
            # Obtener la clave pública
            public_key = child_key.PublicKey().hex()
            
            # Generar dirección según el tipo seleccionado
            tipo = self.addr_type.get()
            direccion = self._generar_direccion_por_tipo(public_key, tipo)
            
            return {
                'indice': indice,
                'direccion': direccion,
                'clave_privada': wif,
                'clave_publica': public_key,
                'tipo': tipo
            }
            
        except Exception as e:
            raise Exception(f"Error al generar la dirección: {str(e)}")
    
    def _generar_direccion_por_tipo(self, public_key_hex, tipo):
        """
        Genera una dirección del tipo especificado a partir de una clave pública.
        
        Args:
            public_key_hex: Clave pública en formato hexadecimal.
            tipo: Tipo de dirección a generar (ADDR_TYPE_*).
            
        Returns:
            str: Dirección Bitcoin generada.
        """
        try:
            # Crear objeto de clave pública
            pub_key = PublicKey.from_hex(public_key_hex)
            
            if tipo == ADDR_TYPE_P2PKH:
                # P2PKH (Legacy) - 1...
                return P2pkhAddress.from_public_key(pub_key).to_string()
                
            elif tipo == ADDR_TYPE_P2SH_P2WPKH:
                # P2SH-P2WPKH (Nested SegWit) - 3...
                return P2shAddress.from_script(
                    P2wpkhAddress.from_public_key(pub_key).to_script_pub_key()
                ).to_string()
                
            elif tipo == ADDR_TYPE_P2WPKH:
                # P2WPKH (Native SegWit) - bc1...
                return P2wpkhAddress.from_public_key(pub_key).to_string()
                
            else:
                raise ValueError(f"Tipo de dirección no soportado: {tipo}")
                
        except Exception as e:
            raise Exception(f"Error al generar dirección {tipo}: {str(e)}")
    
    def _agregar_direccion_a_tabla(self, indice, direccion_info):
        """Agrega una dirección a la tabla de direcciones."""
        self.tree.insert("", tk.END, values=(
            direccion_info['indice'],
            direccion_info['direccion'],
            direccion_info['clave_privada'],
            "0.0"  # Saldo (se actualizaría con una consulta a la blockchain)
        ))
    
    def _limpiar_tabla(self):
        """Limpia la tabla de direcciones."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def _copiar_direccion(self):
        """Copia la dirección seleccionada al portapapeles."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una dirección.")
            return
            
        direccion = self.tree.item(seleccion[0])['values'][1]
        self.clipboard_clear()
        self.clipboard_append(direccion)
        messagebox.showinfo("Copiado", "Dirección copiada al portapapeles.")
    
    def _copiar_clave_privada(self):
        """Copia la clave privada seleccionada al portapapeles."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una dirección.")
            return
            
        clave_privada = self.tree.item(seleccion[0])['values'][2]
        self.clipboard_clear()
        self.clipboard_append(clave_privada)
        messagebox.showinfo("Copiado", "Clave privada copiada al portapapeles.")
    
    def _ver_en_explorador(self):
        """Abre la dirección seleccionada en un explorador de blockchain."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una dirección.")
            return
            
        direccion = self.tree.item(seleccion[0])['values'][1]
        url = f"https://www.blockchain.com/btc/address/{direccion}"
        webbrowser.open(url)
    
    def _nueva_cartera(self):
        """Crea una nueva cartera."""
        if messagebox.askyesno("Nueva Cartera", "¿Está seguro de que desea crear una nueva cartera? Se perderán los datos no guardados."):
            self.semilla = None
            self.direcciones = []
            self.seed_text.delete(1.0, tk.END)
            self._limpiar_tabla()
    
    def _abrir_cartera(self):
        """Abre un archivo de cartera existente."""
        filepath = filedialog.askopenfilename(
            title="Abrir Cartera",
            filetypes=[("Archivos de Cartera", "*.json"), ("Todos los archivos", "*.*")]
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validar el formato del archivo
            if 'semilla' not in data or 'direcciones' not in data:
                raise ValueError("Formato de archivo de cartera inválido")
                
            # Cargar datos
            self.semilla = data['semilla']
            self.direcciones = data['direcciones']
            
            # Actualizar la interfaz
            self.seed_text.delete(1.0, tk.END)
            self.seed_text.insert(tk.END, self.semilla)
            
            self._limpiar_tabla()
            for i, direccion in enumerate(self.direcciones):
                self._agregar_direccion_a_tabla(i, direccion)
                
            messagebox.showinfo("Éxito", f"Cartera cargada correctamente. {len(self.direcciones)} direcciones cargadas.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la cartera: {str(e)}")
    
    def _guardar_cartera_como(self):
        """Guarda la cartera actual en un archivo."""
        if not self.semilla:
            messagebox.showwarning("Advertencia", "No hay datos de cartera para guardar.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos de Cartera", "*.json"), ("Todos los archivos", "*.*")],
            title="Guardar Cartera Como"
        )
        
        if not filepath:
            return
            
        try:
            data = {
                'version': '1.0',
                'fecha_creacion': datetime.now().isoformat(),
                'semilla': self.semilla,
                'direcciones': self.direcciones
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            messagebox.showinfo("Éxito", f"Cartera guardada correctamente en:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la cartera: {str(e)}")
    
    def _mostrar_preferencias(self):
        """Muestra el diálogo de preferencias."""
        dialog = PreferencesDialog(self)
        self.wait_window(dialog)
    
    def _configurar_red(self):
        """Muestra el diálogo de configuración de red."""
        dialog = NetworkSettingsDialog(self)
        self.wait_window(dialog)
    
    def _mostrar_documentacion(self):
        """Abre la documentación en el navegador web."""
        webbrowser.open("https://github.com/tu-usuario/creador-carteras-bitcoin-hd")
    
    def _mostrar_acerca_de(self):
        """Muestra el diálogo Acerca de."""
        about_text = """
Creador de Carteras Bitcoin HD
Versión 1.0.0

Una aplicación para generar y gestionar carteras Bitcoin HD (BIP-32/39/44).

Desarrollado con Python y Tkinter.

© 2023 Tu Nombre
        """.strip()
        
        messagebox.showinfo("Acerca de", about_text)


def main():
    """Función principal de la aplicación."""
    app = CreadorCarterasApp()
    app.mainloop()


if __name__ == "__main__":
    main()
