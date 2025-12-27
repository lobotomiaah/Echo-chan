import os
import importlib

print("🔄 Iniciando carregamento automático do sistema...\n")

total = 0

pastas = [
    p for p in os.listdir()
    if os.path.isdir(p) and os.path.exists(os.path.join(p, "__init__.py"))
]

for pasta in pastas:
    print(f"📂 Carregando pasta: {pasta}")

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".py") and arquivo != "__init__.py":
            try:
                importlib.import_module(f"{pasta}.{arquivo[:-3]}")
                print(f"   ✔ {arquivo}")
                total += 1
            except Exception as e:
                print(f"   ❌ Erro em {arquivo}: {e}")

    print()

print(f"✅ Sistema pronto! {total} módulos carregados com sucesso 🚀")
