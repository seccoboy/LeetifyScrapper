import os

folder_path = "parsed/"

# Loop através de cada arquivo no diretório
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Verifica se o arquivo é um arquivo CSV
    if filename.endswith(".csv"):
        # Leitura do arquivo CSV
        with open(file_path, "r") as file:
            content = file.read()
        
        # Realiza a substituição de ",," por ","
        modified_content = content.replace(",,", ",")
        
        # Salva o arquivo CSV modificado com o mesmo formato
        with open(file_path, "w") as file:
            file.write(modified_content)

print("Virgulas Removidas")