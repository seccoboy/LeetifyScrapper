import os
import pandas as pd

folder_path = "parsed/"

# Loop através de cada arquivo no diretório
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Verifica se o arquivo é um arquivo CSV
    if filename.endswith(".csv"):
        # Leitura do arquivo CSV
        df = pd.read_csv(file_path)
        
        # Seleciona apenas as colunas não em branco, incluindo a primeira coluna
        non_empty_cols = df.columns[df.notna().any()].tolist()
        df = df[non_empty_cols]
        
        # Salva o arquivo CSV modificado, substituindo o original
        df.to_csv(file_path, index=False)

print("Colunas em Branco Formatadas")