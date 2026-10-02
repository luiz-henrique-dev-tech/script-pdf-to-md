import os
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import pymupdf4llm

auth.authenticate_user()
drive_service = build('drive', 'v3')

SOURCE_FOLDER_ID = 'colar_aqui_o_id_da_pasta_de_origem'
DESTINATION_FOLDER_ID = 'colar_aqui_o_id_da_pasta_de_destino'
LAST_FILES = ['arquivos_que_deve_ser_o_penultimo.pdf', 'arquivo_que_deve_ser_o_ultimo.pdf']

def get_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)", pageSize=1000).execute()
    return results.get('files', [])

def download_pdf(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    with open(file_name, 'wb') as f:
        f.write(fh.getvalue())

def extract_text_to_md_advanced(pdf_filename, md_filename):
    try:
        md_text = pymupdf4llm.to_markdown(pdf_filename)
        if not md_text.strip():
            md_text = "> Este arquivo parece ser uma imagem escaneada. Não foi possível extrair texto diretamente via PyMuPDF.\n\n"
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(md_text)
    except Exception as e:
        print(f"Erro ao processar {pdf_filename}: {e}")
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(f"Erro ao extrair o arquivo: {e}")

def upload_to_drive(md_filename, folder_id):
    file_metadata = {'name': md_filename, 'parents': [folder_id]}
    media = MediaFileUpload(md_filename, mimetype='text/markdown')
    drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def main():
    print("Iniciando varredura no Google Drive...")
    files = get_files_in_folder(SOURCE_FOLDER_ID)

    regular_files = []
    last_files_to_process = []
    for f in files:
        if f['name'] in LAST_FILES:
            last_files_to_process.append(f)
        else:
            regular_files.append(f)

    ordered_files = regular_files + last_files_to_process
    print(f"Total de arquivos encontrados: {len(ordered_files)}")

    for idx, f in enumerate(ordered_files, 1):
        file_id = f['id']
        pdf_name = f['name']
        md_name = pdf_name.replace('.pdf', '.md')

        print(f"[{idx}/{len(ordered_files)}] Processando: {pdf_name}...")
        download_pdf(file_id, pdf_name)
        extract_text_to_md_advanced(pdf_name, md_name)
        upload_to_drive(md_name, DESTINATION_FOLDER_ID)

        os.remove(pdf_name)
        os.remove(md_name)

    print("\nProcesso concluído com sucesso!")

if __name__ == '__main__':
    main()
