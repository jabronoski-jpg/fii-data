from datetime import datetime


def _hora():
    return datetime.now().strftime("%H:%M:%S")


def info(texto):
    print(f"[{_hora()}] [INFO] {texto}")


def aviso(texto):
    print(f"[{_hora()}] [AVISO] {texto}")


def erro(texto):
    print(f"[{_hora()}] [ERRO] {texto}")


def linha():
    print("-" * 60)