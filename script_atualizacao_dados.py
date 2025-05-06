import requests
import os
import zipfile
from pathlib import Path
import schedule
import time
from datetime import datetime
import csv

def log_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def download_and_extract(url, folder, retries=5, backoff_factor=0.3):
    file_name = url.split("/")[-1]
    zip_save_path = os.path.join(folder, file_name)
    attempt = 0

    while attempt < retries:
        try:
            print(f"{log_time()} - Iniciando processo para {file_name}")

            # Verifica se o arquivo já existe
            if Path(zip_save_path).exists():
                print(f"{log_time()} - Arquivo {file_name} já existe. Verificando integridade...")
                try:
                    with zipfile.ZipFile(zip_save_path, 'r') as zip_ref:
                        if zip_ref.testzip() is None:
                            print(f"{log_time()} - Arquivo {file_name} está íntegro. Pulando download.")
                            return True
                        else:
                            print(f"{log_time()} - Arquivo {file_name} está corrompido. Será baixado novamente.")
                except zipfile.BadZipFile:
                    print(f"{log_time()} - Arquivo {file_name} é um zip inválido. Será baixado novamente.")
                os.remove(zip_save_path)

            # Faz o download do arquivo
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP não-sucedidos
           
            with open(zip_save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"{log_time()} - Download de {file_name} concluído.")

            # Extraindo o arquivo
            try:
                with zipfile.ZipFile(zip_save_path, 'r') as zip_ref:
                    zip_ref.extractall(folder)
                print(f"{log_time()} - Arquivo {file_name} extraído para {folder}.")
                os.remove(zip_save_path)  # Remove o arquivo zip após a extração
                print(f"{log_time()} - Arquivo {file_name} removido.")
                return True
            except zipfile.BadZipFile:
                print(f"{log_time()} - Falha ao extrair {file_name}. O arquivo está corrompido.")
                return False

        except (requests.exceptions.RequestException, zipfile.BadZipFile) as e:
            attempt += 1
            wait_time = backoff_factor * (2 ** attempt)
            print(f"{log_time()} - Tentativa {attempt} falhou: {e}. Tentando novamente em {wait_time} segundos...")
            time.sleep(wait_time)

    print(f"{log_time()} - Erro ao baixar o arquivo {file_name}. Todas as tentativas falharam.")
    return False

def write_data_carga_csv(folder, file_name):
    # Caminho completo do arquivo
    file_path = os.path.join(folder, file_name)

    if os.path.exists(file_path):
        # Obtém a data de modificação do arquivo
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y')

        # Caminho completo para o novo arquivo
        data_carga_csv = os.path.join(folder, 'data_carga_siconv1.csv')

        # Escreve o CSV com as datas na coluna 'data_carga'
        with open(data_carga_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['data_carga'])
            writer.writerow([datetime.now().strftime('%d/%m/%Y')])  # Data atual
            writer.writerow([mod_time])  # Data de modificação do arquivo

        print(f"{log_time()} - Arquivo {data_carga_csv} criado com sucesso.")
    else:
        print(f"{log_time()} - Arquivo {file_name} não encontrado para obter a data de modificação.")

def job():
    # Lista de URLs dos arquivos a serem baixados
    urls = [
        "http://repositorio.dados.gov.br/seges/detru/siconv_convenio.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_empenho.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_emenda.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_programa.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_programa_proposta.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_desembolso.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_proposta.csv.zip"
    ]
   
    folder = r"C:\Users\willian.j.santos\Desktop\dados"
    os.makedirs(folder, exist_ok=True)

    for url in urls:
        success = download_and_extract(url, folder)
        if success:
            print(f"{log_time()} - Arquivo {url} baixado e extraído com sucesso.")
        else:
            print(f"{log_time()} - Ocorreu um problema durante o download e a extração do arquivo {url}.")

    # Criar o arquivo `data_carga_siconv1.csv` com a data de modificação do arquivo `siconv_proposta.csv`
    write_data_carga_csv(folder, "siconv_proposta.csv")

def schedule_jobs():
    # Executa o job imediatamente ao iniciar o script
    job()

    # Agenda o job para 07:00 da manhã
    schedule.every().day.at("07:00").do(job)

    # Agenda o job para 13:30 da tarde
    schedule.every().day.at("13:30").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Espera 1 minuto entre as verificações

if __name__ == "__main__":
    schedule_jobs()