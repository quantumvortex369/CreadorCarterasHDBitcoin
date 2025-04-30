# Creador de Carteras HD de Bitcoin (BIP39/BIP32)

Este proyecto es una implementación de un generador de carteras HD (Jerárquicas Determinísticas) para Bitcoin, utilizando los estándares BIP39 (para la semilla mnemotécnica) y BIP32 (para la derivación de claves). La herramienta permite generar de manera segura claves privadas, públicas y direcciones Bitcoin asociadas a una semilla mnemotécnica, todo dentro de un entorno Python.

Descripción
---------------
Las carteras HD (Hierarchical Deterministic Wallets) son carteras que generan un árbol de claves derivadas de una semilla mnemotécnica, lo que permite a los usuarios generar direcciones y claves privadas de forma segura y predecible. Este sistema utiliza los estándares BIP39 y BIP32, que son ampliamente aceptados en la comunidad de Bitcoin, para asegurar que las claves y direcciones generadas sean compatibles con otros sistemas y plataformas de Bitcoin.

BIP39: Especifica cómo generar una semilla mnemotécnica que puede ser utilizada para recuperar una cartera.

BIP32: Define un esquema jerárquico para derivar claves privadas y públicas a partir de una semilla de forma determinística.

Características
----------------
Generación de semilla mnemotécnica (12 palabras): Utiliza BIP39 para crear una semilla de recuperación fácil de recordar.

Derivación de claves privadas y públicas: Usando BIP32, se derivan claves privadas y públicas a partir de la semilla mnemotécnica.

Generación de direcciones Bitcoin: A partir de la clave pública generada, el script calcula la dirección Bitcoin en formato Base58.

Fácil de usar: Solo necesitas ejecutar el script para obtener tu semilla mnemotécnica, claves y dirección Bitcoin.

Requisitos
----------------
Para ejecutar este proyecto, necesitas tener instalado Python y las siguientes librerías:

mnemonic: Para la generación de semillas mnemotécnicas BIP39.

bip32utils: Para la derivación de claves privadas y públicas BIP32.

base58: Para la conversión de la dirección Bitcoin al formato Base58.



Puedes instalar las dependencias con el siguiente comando:
pip install mnemonic bip32utils base58


Instrucciones de uso
----------------------
1- Clona este repositorio en tu máquina local o descarga el archivo CreadorCarterasHD.py.

2- Abre una terminal en la ubicación donde descargaste el archivo.

3- Ejecuta el script con el siguiente comando:
python CreadorCarterasHD.py

4-El script generará lo siguiente:

- Semilla mnemotécnica (12 palabras) que podrás usar para respaldar tu cartera.

- Clave privada en formato hexadecimal, que te da acceso completo a tu cartera.

- Clave pública en formato hexadecimal, que es utilizada para generar direcciones y recibir fondos.

- Dirección Bitcoin en formato Base58 que podrás usar para recibir pagos.

  

Ejemplo de salida:
---------------------

Semilla generada: 
    "wheat rent dwarf price shock health soap sort print whale taxi magic"

Clave privada: 
    "c0a1d1e44b607e83d9ecb214a83a84eaf27e51769b8e99e1bb1fe8d6c1986e71"

Clave pública: 
    "0359c3c73cf474c7f0ad2b45a490a6d94d8d2fe3d7bfbebdd0b3897e7597f78f30"

Dirección Bitcoin:
    "1Lb4v4DzXH6n92Y2f5pk6h6o5Ra9U5gXBk"


Explicación del código
------------------------
Generación de la semilla mnemotécnica: El script usa la librería mnemonic para generar una semilla BIP39 de 128 bits (12 palabras). Esta semilla es la base para la creación de todas las claves y direcciones asociadas a la cartera.

Derivación de claves privadas y públicas: Utiliza la librería bip32utils para derivar claves privadas y públicas a partir de la semilla mnemotécnica. Se sigue el estándar BIP32, donde se usa la ruta m/44'/0'/0'/0 para generar claves según el protocolo de Bitcoin.

Generación de la dirección Bitcoin: Se calcula la dirección Bitcoin a partir de la clave pública usando una combinación de SHA256 y RIPEMD160, seguida de un cálculo de checksum y la conversión del resultado en formato Base58.

Seguridad
-----------
Respaldo de la semilla: La semilla mnemotécnica es la única forma de restaurar el acceso a la cartera. Asegúrate de guardarla de manera segura, fuera del alcance de terceros.

Clave privada: La clave privada debe mantenerse en secreto. Si alguien tiene acceso a tu clave privada, podrá acceder a tus fondos.

Dirección pública: La dirección pública puede compartirse sin riesgo. Esta dirección es solo para recibir pagos.
