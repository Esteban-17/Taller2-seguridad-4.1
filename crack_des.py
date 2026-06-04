#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
 Taller 2 - Seguridad Computacional (UPTC)
 Punto 4.1 - Recuperacion de contrasenas por fuerza bruta

 Requisito UNICO:   pip install passlib
====================================================================
"""

import itertools
import time
import string
from passlib.hash import des_crypt   # DES crypt(3) en Python puro

# --------------------------------------------------------------------
# 1) Alfabetos, de menor a mayor tamano
# --------------------------------------------------------------------
ALFABETOS = [
    ("minusculas",   string.ascii_lowercase),                                 # 26
    ("minus+mayus",  string.ascii_letters),                                   # 52
    ("alfanumerico", string.ascii_letters + string.digits),                   # 62
    ("completo",     string.ascii_letters + string.digits + string.punctuation),  # 94
]

# --------------------------------------------------------------------
# 2) Tabla entregada: (hash_completo, longitud_de_la_contrasena)
# --------------------------------------------------------------------
OBJETIVOS = [
    ("ok/gej3.yEFeI", 3),
    ("Aa40nuCvdYzJA", 3),
    ("k+FCC/vC42ryg", 3),   # sal con '+' -> no valida en DES estandar
    ("2K8b.xipQrzNg", 3),
    ("kot8Y1NRfX2.w", 4),
    ("4aibIYop66j9w", 5),
    ("UPUKXy9WwFGYI", 4),
]


def romper(hash_objetivo: str, longitud: int):
    t0 = time.time()

    # passlib.verify() compara un candidato contra el hash y extrae la sal solo.
    # Si la sal del hash es invalida, lanza ValueError -> lo capturamos.
    try:
        des_crypt.verify("test", hash_objetivo)
    except ValueError:
        return None, "SAL_INVALIDA", time.time() - t0

    for nombre, alfabeto in ALFABETOS:
        for combo in itertools.product(alfabeto, repeat=longitud):
            candidato = "".join(combo)
            if des_crypt.verify(candidato, hash_objetivo):
                return candidato, nombre, time.time() - t0
    return None, None, time.time() - t0


def main():
    print("=" * 68)
    print(" RECUPERACION DE CONTRASENAS")
    print("=" * 68)
    print(f"{'HASH':<16}{'LARGO':<7}{'CLAVE':<14}{'ALFABETO':<16}{'TIEMPO'}")
    print("-" * 68)
    for h, n in OBJETIVOS:
        clave, alf, dt = romper(h, n)
        clave_txt = clave if clave else "NO RECUPERADA"
        print(f"{h:<16}{n:<7}{clave_txt:<14}{str(alf):<16}{dt:.2f}s")


if __name__ == "__main__":
    main()
