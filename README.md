# 📄 PDF to Markdown Extractor (for LLMs)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Um script automatizado feito para rodar no Google Colab que converte pastas inteiras de PDFs do Google Drive em arquivos Markdown (`.md`) perfeitamente estruturados.

Ideal para preparar documentos para **RAG (Retrieval-Augmented Generation)** e análise por **LLMs**, pois utiliza a biblioteca `pymupdf4llm` para preservar tabelas, cabeçalhos e listas, economizando tokens e mantendo o contexto da formatação original.

## 🚀 Funcionalidades

- **Processamento em Lote:** Converte dezenas de PDFs de uma vez de forma autônoma.
- **Integração Nativa:** Lê de uma pasta no Google Drive e salva os `.md` direto em outra.
- **Otimizado para IA:** Mantém a estrutura de formatação original usando PyMuPDF.
- **Tratamento de Exceções:** Identifica PDFs escaneados (sem camada de texto) e alerta o usuário.
- **Fila de Prioridade:** Permite definir arquivos específicos para serem processados por último.

## 🛠️ Como usar (Google Colab)

A maneira mais fácil de rodar este extrator é no Google Colab. Nenhuma instalação local é necessária.

1. Crie um novo notebook no [Google Colab](https://colab.research.google.com/).
2. Copie o conteúdo de `pdf_to_md_extractor.py` e cole na primeira célula.
3. Adicione a seguinte linha no topo da célula para instalar as dependências:
   ```python
   !pip install pymupdf4llm pymupdf google-api-python-client
   ```
4. Substitua as variáveis de configuração pelas IDs das suas pastas no Drive:
   ```python
   SOURCE_FOLDER_ID = 'id_da_sua_pasta_com_pdfs'
   DESTINATION_FOLDER_ID = 'id_da_sua_pasta_de_destino'
   ```
   > 💡 O ID da pasta é o trecho final da URL quando você a abre no navegador:
   > `https://drive.google.com/drive/folders/**ESTE_TRECHO_É_O_ID**`
5. (Opcional) Liste em `LAST_FILES` os nomes dos arquivos `.pdf` que devem ser processados por último, caso queira priorizar os demais.
6. Execute a célula. Na primeira execução, o Colab solicitará autorização para acessar sua conta do Google Drive — basta aprovar.
7. Acompanhe o progresso pelos logs impressos no notebook. Ao final, os arquivos `.md` estarão na pasta de destino configurada.

## 📋 Requisitos

- Conta Google com acesso ao Google Drive.
- Permissão de leitura na pasta de origem e de escrita na pasta de destino.
- Bibliotecas instaladas automaticamente pelo Colab: `pymupdf4llm`, `pymupdf`, `google-api-python-client`.

## ⚠️ Observações

- PDFs puramente escaneados (sem camada de texto) não são convertidos automaticamente; o script gera um arquivo `.md` com um aviso indicando que o OCR não foi aplicado.
- Os arquivos PDF e Markdown são processados e removidos do ambiente temporário do Colab a cada iteração, mantendo o uso de disco baixo.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias, correções ou novas funcionalidades.

## 📄 Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
