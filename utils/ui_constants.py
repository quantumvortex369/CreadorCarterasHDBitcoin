"""
Constantes para la interfaz de usuario del Creador de Carteras Cripto HD.
"""

# Configuración de temas
THEMES = {
    'light': {
        'name': 'Claro',
        'bg': '#f0f0f0',
        'fg': '#000000',
        'accent': '#0078d7',
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'highlight': '#e9f5ff',
        'border': '#c0c0c0',
        'text': '#212529',
        'disabled': '#6c757d',
        'select_bg': '#d4e6f5',
        'select_fg': '#000000',
        'button_bg': '#e0e0e0',
        'button_fg': '#000000',
        'button_active_bg': '#c0c0c0',
        'button_active_fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'entry_select_bg': '#4a98e0',
        'entry_select_fg': '#ffffff',
        'tab_bg': '#e0e0e0',
        'tab_fg': '#000000',
        'tab_active_bg': '#f0f0f0',
        'tab_active_fg': '#000000',
        'menu_bg': '#f0f0f0',
        'menu_fg': '#000000',
        'menu_active_bg': '#e0e0e0',
        'menu_active_fg': '#000000',
        'scrollbar_bg': '#e0e0e0',
        'scrollbar_trough': '#f0f0f0',
        'scrollbar_arrow': '#000000',
        'tree_bg': '#ffffff',
        'tree_fg': '#000000',
        'tree_selected_bg': '#4a98e0',
        'tree_selected_fg': '#ffffff',
        'tree_arrow': '#000000',
        'separator': '#c0c0c0',
        'tooltip_bg': '#ffffe1',
        'tooltip_fg': '#000000',
        'tooltip_border': '#000000'
    },
    'dark': {
        'name': 'Oscuro',
        'bg': '#2d2d2d',
        'fg': '#e0e0e0',
        'accent': '#4a98e0',
        'success': '#5cb85c',
        'warning': '#f0ad4e',
        'error': '#d9534f',
        'highlight': '#3a3a3a',
        'border': '#4a4a4a',
        'text': '#f8f9fa',
        'disabled': '#6c757d',
        'select_bg': '#1e4a6e',
        'select_fg': '#ffffff',
        'button_bg': '#3a3a3a',
        'button_fg': '#e0e0e0',
        'button_active_bg': '#4a4a4a',
        'button_active_fg': '#ffffff',
        'entry_bg': '#3a3a3a',
        'entry_fg': '#e0e0e0',
        'entry_select_bg': '#4a98e0',
        'entry_select_fg': '#ffffff',
        'tab_bg': '#3a3a3a',
        'tab_fg': '#e0e0e0',
        'tab_active_bg': '#2d2d2d',
        'tab_active_fg': '#ffffff',
        'menu_bg': '#3a3a3a',
        'menu_fg': '#e0e0e0',
        'menu_active_bg': '#4a4a4a',
        'menu_active_fg': '#ffffff',
        'scrollbar_bg': '#4a4a4a',
        'scrollbar_trough': '#2d2d2d',
        'scrollbar_arrow': '#e0e0e0',
        'tree_bg': '#3a3a3a',
        'tree_fg': '#e0e0e0',
        'tree_selected_bg': '#4a98e0',
        'tree_selected_fg': '#ffffff',
        'tree_arrow': '#e0e0e0',
        'separator': '#4a4a4a',
        'tooltip_bg': '#4a4a4a',
        'tooltip_fg': '#e0e0e0',
        'tooltip_border': '#6c757d'
    }
}

# Configuración de idiomas
LANGUAGES = {
    'es': 'Español',
    'en': 'English',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'zh': '中文',
    'ja': '日本語',
    'ko': '한국어'
}

# Tamaños de fuente
FONT_SIZES = {
    'small': {'size': 9},
    'normal': {'size': 10},
    'large': {'size': 11},
    'xlarge': {'size': 12},
    'title': {'size': 14, 'weight': 'bold'},
    'heading': {'size': 16, 'weight': 'bold'},
    'subheading': {'size': 12, 'weight': 'bold'},
    'mono': {'family': 'Courier New', 'size': 10}
}

# Estilos de botones
BUTTON_STYLES = {
    'primary': {
        'background': '#0078d7',
        'foreground': '#ffffff',
        'activebackground': '#005a9e',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'bold')
    },
    'secondary': {
        'background': '#6c757d',
        'foreground': '#ffffff',
        'activebackground': '#5a6268',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'normal')
    },
    'success': {
        'background': '#28a745',
        'foreground': '#ffffff',
        'activebackground': '#218838',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'bold')
    },
    'danger': {
        'background': '#dc3545',
        'foreground': '#ffffff',
        'activebackground': '#c82333',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'bold')
    },
    'warning': {
        'background': '#ffc107',
        'foreground': '#212529',
        'activebackground': '#e0a800',
        'activeforeground': '#212529',
        'font': ('Arial', 10, 'bold')
    },
    'info': {
        'background': '#17a2b8',
        'foreground': '#ffffff',
        'activebackground': '#138496',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'bold')
    },
    'light': {
        'background': '#f8f9fa',
        'foreground': '#212529',
        'activebackground': '#e2e6ea',
        'activeforeground': '#212529',
        'font': ('Arial', 10, 'normal')
    },
    'dark': {
        'background': '#343a40',
        'foreground': '#ffffff',
        'activebackground': '#23272b',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'normal')
    }
}

# Estilos de entrada
ENTRY_STYLES = {
    'default': {
        'background': '#ffffff',
        'foreground': '#212529',
        'selectbackground': '#4a98e0',
        'selectforeground': '#ffffff',
        'insertbackground': '#212529',
        'font': ('Arial', 10, 'normal'),
        'borderwidth': 1,
        'relief': 'flat',
        'padding': (5, 5)
    },
    'readonly': {
        'background': '#e9ecef',
        'foreground': '#6c757d',
        'selectbackground': '#4a98e0',
        'selectforeground': '#ffffff',
        'insertbackground': '#6c757d',
        'font': ('Arial', 10, 'normal'),
        'borderwidth': 1,
        'relief': 'flat',
        'readonlybackground': '#e9ecef'
    },
    'valid': {
        'background': '#e8f5e9',
        'foreground': '#2e7d32',
        'font': ('Arial', 10, 'normal')
    },
    'invalid': {
        'background': '#ffebee',
        'foreground': '#c62828',
        'font': ('Arial', 10, 'normal')
    },
    'disabled': {
        'background': '#e9ecef',
        'foreground': '#6c757d',
        'font': ('Arial', 10, 'normal')
    }
}

# Estilos de etiquetas
LABEL_STYLES = {
    'default': {
        'font': ('Arial', 10, 'normal'),
        'foreground': '#212529',
        'background': '',
        'anchor': 'w'
    },
    'title': {
        'font': ('Arial', 14, 'bold'),
        'foreground': '#212529',
        'background': '',
        'anchor': 'w'
    },
    'heading': {
        'font': ('Arial', 12, 'bold'),
        'foreground': '#212529',
        'background': '',
        'anchor': 'w'
    },
    'subheading': {
        'font': ('Arial', 11, 'bold'),
        'foreground': '#343a40',
        'background': '',
        'anchor': 'w'
    },
    'success': {
        'font': ('Arial', 10, 'normal'),
        'foreground': '#28a745',
        'background': '',
        'anchor': 'w'
    },
    'error': {
        'font': ('Arial', 10, 'normal'),
        'foreground': '#dc3545',
        'background': '',
        'anchor': 'w'
    },
    'warning': {
        'font': ('Arial', 10, 'normal'),
        'foreground': '#ffc107',
        'background': '',
        'anchor': 'w'
    },
    'info': {
        'font': ('Arial', 10, 'normal'),
        'foreground': '#17a2b8',
        'background': '',
        'anchor': 'w'
    },
    'muted': {
        'font': ('Arial', 9, 'normal'),
        'foreground': '#6c757d',
        'background': '',
        'anchor': 'w'
    },
    'mono': {
        'font': ('Courier New', 10, 'normal'),
        'foreground': '#212529',
        'background': '',
        'anchor': 'w'
    }
}

# Estilos de marcos
FRAME_STYLES = {
    'default': {
        'background': '#f8f9fa',
        'borderwidth': 1,
        'relief': 'flat',
        'padx': 5,
        'pady': 5
    },
    'raised': {
        'background': '#f8f9fa',
        'borderwidth': 1,
        'relief': 'raised',
        'padx': 5,
        'pady': 5
    },
    'sunken': {
        'background': '#f8f9fa',
        'borderwidth': 1,
        'relief': 'sunken',
        'padx': 5,
        'pady': 5
    },
    'flat': {
        'background': '#f8f9fa',
        'borderwidth': 0,
        'relief': 'flat',
        'padx': 5,
        'pady': 5
    },
    'toolbar': {
        'background': '#e9ecef',
        'borderwidth': 0,
        'relief': 'flat',
        'padx': 5,
        'pady': 2
    },
    'statusbar': {
        'background': '#e9ecef',
        'borderwidth': 1,
        'relief': 'sunken',
        'padx': 5,
        'pady': 2
    }
}

# Estilos de pestañas
NOTEBOOK_STYLES = {
    'default': {
        'background': '#f8f9fa',
        'borderwidth': 0,
        'padding': (5, 5, 5, 5)
    },
    'tab': {
        'padding': (10, 5),
        'font': ('Arial', 10, 'normal')
    },
    'selected': {
        'background': '#ffffff',
        'foreground': '#0078d7',
        'font': ('Arial', 10, 'bold')
    },
    'unselected': {
        'background': '#e9ecef',
        'foreground': '#6c757d',
        'font': ('Arial', 10, 'normal')
    }
}

# Estilos de árbol
TREEVIEW_STYLES = {
    'default': {
        'background': '#ffffff',
        'foreground': '#212529',
        'fieldbackground': '#ffffff',
        'font': ('Arial', 10, 'normal'),
        'borderwidth': 1,
        'relief': 'flat',
        'rowheight': 25,
        'show': 'tree headings'
    },
    'header': {
        'background': '#e9ecef',
        'foreground': '#212529',
        'font': ('Arial', 10, 'bold'),
        'relief': 'raised',
        'borderwidth': 1
    },
    'row': {
        'background': '#ffffff',
        'foreground': '#212529',
        'font': ('Arial', 10, 'normal')
    },
    'selected': {
        'background': '#4a98e0',
        'foreground': '#ffffff',
        'font': ('Arial', 10, 'normal')
    },
    'alternate': {
        'background': '#f8f9fa'
    },
    'disabled': {
        'foreground': '#6c757d',
        'font': ('Arial', 10, 'normal')
    }
}

# Estilos de barra de desplazamiento
SCROLLBAR_STYLES = {
    'vertical': {
        'width': 16,
        'arrowsize': 14,
        'troughcolor': '#e9ecef',
        'background': '#adb5bd',
        'bordercolor': '#e9ecef',
        'arrowcolor': '#6c757d',
        'activebackground': '#6c757d',
        'troughrelief': 'flat',
        'relief': 'flat'
    },
    'horizontal': {
        'height': 16,
        'arrowsize': 14,
        'troughcolor': '#e9ecef',
        'background': '#adb5bd',
        'bordercolor': '#e9ecef',
        'arrowcolor': '#6c757d',
        'activebackground': '#6c757d',
        'troughrelief': 'flat',
        'relief': 'flat'
    }
}

# Estilos de menú
MENU_STYLES = {
    'menubar': {
        'background': '#f8f9fa',
        'foreground': '#212529',
        'activebackground': '#e9ecef',
        'activeforeground': '#000000',
        'disabledforeground': '#6c757d',
        'font': ('Arial', 10, 'normal'),
        'relief': 'flat',
        'borderwidth': 0,
        'activeborderwidth': 0
    },
    'menu': {
        'background': '#ffffff',
        'foreground': '#212529',
        'activebackground': '#4a98e0',
        'activeforeground': '#ffffff',
        'disabledforeground': '#6c757d',
        'font': ('Arial', 10, 'normal'),
        'relief': 'flat',
        'borderwidth': 1,
        'activeborderwidth': 0,
        'tearoff': 0
    },
    'menuitem': {
        'background': 'transparent',
        'foreground': '#212529',
        'activebackground': '#4a98e0',
        'activeforeground': '#ffffff',
        'font': ('Arial', 10, 'normal'),
        'padding': (8, 16, 8, 8)
    },
    'separator': {
        'background': '#e9ecef'
    }
}

# Estilos de mensajes
MESSAGE_STYLES = {
    'info': {
        'icon': 'info',
        'background': '#e7f5ff',
        'foreground': '#1864ab',
        'iconcolor': '#1864ab',
        'border': '#d0ebff',
        'font': ('Arial', 10, 'normal')
    },
    'success': {
        'icon': 'check',
        'background': '#ebfbee',
        'foreground': '#2b8a3e',
        'iconcolor': '#2b8a3e',
        'border': '#d3f9d8',
        'font': ('Arial', 10, 'normal')
    },
    'warning': {
        'icon': 'warning',
        'background': '#fff9db',
        'foreground': '#e67700',
        'iconcolor': '#e67700',
        'border': '#ffec99',
        'font': ('Arial', 10, 'normal')
    },
    'error': {
        'icon': 'error',
        'background': '#fff5f5',
        'foreground': '#c92a2a',
        'iconcolor': '#c92a2a',
        'border': '#ffc9c9',
        'font': ('Arial', 10, 'normal')
    }
}
