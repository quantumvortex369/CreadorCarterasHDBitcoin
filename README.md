# 🚀 Creador de Carteras Bitcoin HD

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Una aplicación de escritorio segura para generar y gestionar carteras Bitcoin HD (BIP-32/39/44) con soporte para múltiples tipos de direcciones.

## 🔍 Vista Previa

![Captura de pantalla de la aplicación](screenshot.png)

## ✨ Características Principales

- 🔐 Generación segura de frases mnemotécnicas (12/24 palabras)
- 💼 Soporte para múltiples tipos de direcciones:
  - 🔵 P2PKH (Legacy - Comienza con 1...)
  - 🟠 P2SH (Nested SegWit - Comienza con 3...)
  - 🟢 P2WPKH (Native SegWit - Comienza con bc1...)
- 📋 Generación de códigos QR para direcciones
- 📤 Exportación en múltiples formatos (JSON, texto, PDF, CSV)
- 🎨 Interfaz intuitiva con temas claros/oscuros
- 🔄 Validación integrada de direcciones y claves
- 🔄 Soporte para múltiples idiomas

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Conexión a Internet (solo para verificar direcciones)

## 📥 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/creador-carteras-bitcoin-hd.git
   cd creador-carteras-bitcoin-hd
   ```

2. **Crea y activa un entorno virtual** (altamente recomendado):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Uso

1. **Inicia la aplicación**:
   ```bash
   python CreadorCarterasBitcoinHD.py
   ```

2. **Genera una nueva semilla** o importa una existente
3. **Selecciona el tipo de dirección** deseado
4. **Genera direcciones** según sea necesario
5. **Exporta** tus direcciones de forma segura

## 🏗️ Estructura del Proyecto

```
CreadorCarterasHDBitcoin-main/
├── assets/                  # Recursos estáticos (imágenes, iconos, etc.)
│   ├── images/             # Imágenes de la aplicación
│   └── icons/              # Íconos de la aplicación
├── dialogs/                 # Diálogos de la interfaz de usuario
│   ├── __init__.py
│   ├── network_settings_dialog.py
│   └── preferences_ui.py
├── ui/                      # Módulos de la interfaz de usuario
│   ├── __init__.py
│   ├── transaction_ui.py
│   └── wallet_ui.py
├── utils/                   # Utilidades y constantes
│   ├── __init__.py
│   ├── ui_utils.py
│   ├── ui_utils_part2.py
│   ├── ui_utils_part3.py
│   └── ui_constants.py
├── tests/                   # Pruebas unitarias
│   ├── __init__.py
│   └── test_wallet.py
├── docs/                    # Documentación adicional
│   └── README.md
├── CreadorCarterasBitcoinHD.py  # Aplicación principal
├── __main__.py              # Punto de entrada del paquete
├── config.py                # Configuración de la aplicación
├── crypto_constants.py      # Constantes criptográficas
├── requirements.txt         # Dependencias del proyecto
├── setup.py                 # Configuración del paquete
├── README.md                # Este archivo
├── CHANGELOG.md             # Registro de cambios
├── LICENSE                  # Licencia del proyecto
└── SECURITY.md             # Política de seguridad
```

## 🛠️ Tecnologías utilizadas

- **Python 3.8+** - Lenguaje de programación
- **Tkinter** - Interfaz gráfica
- **bip32utils** - Derivación de claves HD
- **mnemonic** - Generación de semillas BIP39
- **qrcode** - Generación de códigos QR
- **Pillow** - Procesamiento de imágenes para códigos QR

## 📚 Estándares implementados

- **BIP-39**: Semillas mnemotécnicas para generación determinista
- **BIP-32**: Carteras jerárquicas deterministas
- **BIP-44**: Estructura de rutas para cuentas HD
- **BIP-49**: Derivación para direcciones P2SH-P2WPKH (Nested SegWit)
- **BIP-84**: Derivación para direcciones P2WPKH (Native SegWit)

## 🤝 Contribución

Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

Desarrollado con ❤️ para la comunidad Bitcoin

**Importante**: La clave privada debe mantenerse en secreto. Si alguien tiene acceso a tu clave privada, podrá acceder a tus fondos.

**Nota**: La dirección pública puede compartirse sin riesgo. Esta dirección es solo para recibir pagos.
