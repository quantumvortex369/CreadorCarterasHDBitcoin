import mnemonic
from bip32utils import BIP32Key
import hashlib
import base58

# Función para generar la semilla mnemotécnica
def generar_semilla():
    m = mnemonic.Mnemonic("english")  # Usamos el idioma inglés para la semilla
    semilla = m.generate(strength=128)  # Fuerza de 128 bits = 12 palabras
    return semilla

# Función para derivar claves privadas y públicas desde la semilla
def derivar_claves(semilla, indice=0):
    m = mnemonic.Mnemonic("english")
    seed = m.to_seed(semilla, passphrase="")  # Convertimos la semilla a semilla binaria
    bip32 = BIP32Key.fromEntropy(seed)
    
    # Derivamos la clave privada y pública con la ruta estándar m/44'/0'/0'/0 (BIP44)
    clave_privada = bip32.ChildKey(44 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(indice).PrivateKey()
    clave_publica = bip32.ChildKey(44 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(indice).PublicKey()
    
    return clave_privada.hex(), clave_publica.hex()

# Función para generar la dirección Bitcoin a partir de la clave pública
def generar_direccion(clave_publica):
    # Paso 1: Hacer un hash SHA256 de la clave pública
    sha256_hash = hashlib.sha256(bytes.fromhex(clave_publica)).digest()
    
    # Paso 2: Hacer un hash RIPEMD-160 del resultado anterior
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    # Paso 3: Agregar el prefijo 0x00 (para direcciones estándar de Bitcoin)
    prefijo = b'\x00'
    ripemd160_prefixed = prefijo + ripemd160_hash
    
    # Paso 4: Calcular el checksum (primeros 4 bytes del hash SHA256 de la cadena anterior)
    checksum = hashlib.sha256(hashlib.sha256(ripemd160_prefixed).digest()).digest()[:4]
    
    # Paso 5: Crear la dirección final añadiendo el checksum
    direccion_binaria = ripemd160_prefixed + checksum
    
    # Paso 6: Convertir a formato Base58
    direccion_base58 = base58.b58encode(direccion_binaria).decode('utf-8')
    
    return direccion_base58

# Mostrar todo el proceso
def crear_cartera():
    semilla = generar_semilla()
    print("Semilla generada:", semilla)
    
    clave_privada, clave_publica = derivar_claves(semilla)
    print("\nClave privada:", clave_privada)
    print("Clave pública:", clave_publica)
    
    # Generar la dirección Bitcoin a partir de la clave pública
    direccion_bitcoin = generar_direccion(clave_publica)
    print("\nDirección Bitcoin:", direccion_bitcoin)

# Ejecutar el generador de carteras
crear_cartera()
