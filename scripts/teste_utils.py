from utils import *

lista = list(range(25))

print("Lotes:")

for lote in dividir_em_lotes(lista, 10):
    print(lote)

print()

print("Data ISO:")

print(agora_iso())