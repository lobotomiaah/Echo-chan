import os
import importlib
import json

print(" Iniciando carregamento automático do sistema...\n")

total_modulos = 0
dados = {}

pastas = [
    p for p in os.listdir()
    if os.path.isdir(p) and os.path.exists(os.path.join(p, "__init__.py"))
]

for pasta in pastas:
    print(f" Carregando pasta: {pasta}")

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".py") and arquivo != "__init__.py":
            try:
                importlib.import_module(f"{pasta}.{arquivo[:-3]}")
                print(f"   ✔ {arquivo}")
                total_modulos += 1
            except Exception as e:
                print(f"    Erro em {arquivo}: {e}")

    print()

print(" Carregando dados...\n")

pasta_data = "data"

if os.path.exists(pasta_data):
    for arquivo in os.listdir(pasta_data):
        if arquivo.endswith(".json"):
            caminho = os.path.join(pasta_data, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados[arquivo] = json.load(f)
                print(f"   ✔ {arquivo} carregado")
            except Exception as e:
                print(f"   ❌ Erro em {arquivo}: {e}")
else:
    print(" Pasta 'data' não encontrada")
print("\n Sistema pronto!")
print(f" Módulos carregados: {total_modulos}")
print(f" Arquivos de dados carregados: {len(dados)}")
print(" Echo-sama online\n")
