# Recuperación de Contraseñas por Fuerza Bruta — DES `crypt(3)`

Taller 2 · **Electiva IV: Seguridad Computacional**
Universidad Pedagógica y Tecnológica de Colombia (UPTC) — Punto 4.1

---

## Descripción

Herramienta educativa que demuestra la **debilidad de los hashes DES `crypt(3)`**
de Unix frente a ataques de fuerza bruta. El programa toma una lista de hashes
(con su sal incluida en los dos primeros caracteres) y recupera la contraseña
original generando candidatos sistemáticamente y comparándolos contra cada hash.

El ejercicio forma parte de una auditoría simulada cuyo objetivo es evidenciar,
de forma cuantitativa, por qué este esquema de almacenamiento se considera
obsoleto para proteger contraseñas.

> ⚠️ **Uso exclusivamente académico.** Este código se desarrolló como parte de
> un trabajo universitario. Úsalo únicamente sobre datos propios o de prueba.

---

## ¿Cómo funciona?

Un hash es una función de **un solo sentido**: no se puede invertir. El ataque
reproduce el cálculo en sentido directo:

1. Extrae la **sal** del hash objetivo (los 2 primeros caracteres).
2. Genera candidatos con `itertools.product` sobre un alfabeto y una longitud.
3. Hashea cada candidato con la **misma sal** y lo compara con el objetivo.
4. Si coinciden, la contraseña fue recuperada.

Los alfabetos se prueban **de menor a mayor tamaño** (minúsculas → +mayúsculas →
alfanumérico → con símbolos) para no recorrer espacios grandes cuando la clave
es sencilla.

---

## Requisitos

- Python 3.8 o superior (probado en **Python 3.14**).
- Librería [`passlib`](https://pypi.org/project/passlib/).

> Se usa `passlib` porque implementa DES `crypt(3)` en **Python puro**, lo que
> permite ejecutar el programa en Windows. El módulo estándar `crypt` solo
> existe en Unix/Linux y **fue eliminado en Python 3.13**.

---

## Instalación

```bash
pip install passlib
```

O usando el archivo de dependencias incluido:

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
python crack_des.py
```

### Salida esperada

```
====================================================================
 RECUPERACION DE CONTRASENAS
====================================================================
HASH            LARGO  CLAVE         ALFABETO        TIEMPO
--------------------------------------------------------------------
ok/gej3.yEFeI   3      sol           minusculas      0.14s
Aa40nuCvdYzJA   3      TiC           minus+mayus     1.48s
k+FCC/vC42ryg   3      NO RECUPERADA SAL_INVALIDA    0.00s
2K8b.xipQrzNg   3      14#           completo        8.85s
kot8Y1NRfX2.w   4      alex          minusculas      0.07s
4aibIYop66j9w   5      peace         minusculas      69.54s
UPUKXy9WwFGYI   4      UPTC          minus+mayus     70.29s
```

*(Los tiempos varían según el equipo.)*

---

## Nota técnica: el registro `k+FCC/vC42ryg`

Este hash **no se puede reproducir** porque su sal contiene el carácter `+`,
que **no pertenece al alfabeto de sal válido de DES** (`./0-9A-Za-z`, 64
caracteres). Tanto la implementación nativa de Unix como `passlib` lo rechazan
por sal inválida. Esto indica que el hash fue generado por una implementación
de `crypt(3)` no estándar, o que se trata de un error de transcripción en los
datos auditados.

---

## Estructura del repositorio

```
.
├── crack_des.py        # Programa principal
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

---

## Fundamento teórico (resumido)

DES es un cifrador de bloque simétrico con clave efectiva de **56 bits**. La
función `crypt(3)` aplica DES de forma iterada (25 veces) usando la contraseña
como clave, y antepone una sal de 12 bits al resultado de 13 caracteres. Su
debilidad radica en el espacio de clave reducido y en la velocidad de cálculo,
que hacen barato el ataque por fuerza bruta. Los esquemas modernos —bcrypt,
scrypt, Argon2— corrigen esto con un factor de coste configurable y sales más
extensas.

---

## Autor

Daniel — Ingeniería de Sistemas y Computación, UPTC.
