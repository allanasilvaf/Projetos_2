# GAMBOT - Chatbot da plataforma Gam.py

**Assistente Acadêmico Inteligente da Universidade Federal do Pará**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

## Sobre o Projeto

O **Gambot UFPA** é um sistema inteligente de busca e consulta a documentos acadêmicos da UFPA (como regulamentos e grades curriculares). Ele combina:

- **Busca tradicional** por palavras-chave em PDFs.
- **Inteligência Artificial (RAG)** para respostas contextualizadas.
- **Base de conhecimento** focada em documentos oficiais.
- **Sistema híbrido** de pontuação para encontrar a página mais relevante.

### Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|-----------|
| **Busca por Ranking** | Analisa qual página tem mais termos relevantes e densidade de palavras |
| **IA Contextual** | Envia páginas completas para o GPT responder com precisão |
| **Controle de Fontes** | Cita o documento e a página de onde a informação foi retirada |


## Começando Rápido

### Pré-requisitos

- Python 3.8 ou superior
- Git instalado
- Conta na [OpenAI](https://platform.openai.com/) (para API Key)
- PDFs com regulamentos/grade curricular da UFPA

### Instalação Passo a Passo

Siga os comandos abaixo no seu terminal:

**1. Clone o repositório**

git clone [https://github.com/allanasilvaf/gam-py.git](https://github.com/allanasilvaf/gam-py.git)
cd gam-py/backend/modulo_rag
(Ajuste o caminho do cd conforme a estrutura exata da sua pasta)

2. Crie e ative o ambiente virtual (Recomendado) Isso isola as dependências do projeto para não conflitar com seu sistema.

No Windows:

python -m venv venv
.\venv\Scripts\activate

No Linux/Mac:

python3 -m venv venv
source venv/bin/activate
3. Instale as dependências

pip install -r requirements.txt
⚙️ Configuração
Adicione seus PDFs Coloque os arquivos PDF (Regulamento, Grade, PPC) dentro da pasta data/.

Se a pasta não existir, o sistema criará automaticamente na primeira execução, mas você precisará adicionar os arquivos nela.

Configure a API Key Crie um arquivo chamado api_key.env na raiz do projeto (onde está o app.py) e adicione sua chave:

Snippet de código

OPENAI_API_KEY=sk-sua-chave-aqui-123456...
MODEL=gpt-4o-mini
...

▶️ Executando o Sistema
Com o ambiente virtual ativado e as configurações feitas, execute:

streamlit run app.py
O sistema abrirá automaticamente no seu navegador em: http://localhost:8501

 Como Usar
 
1. Configuração Inicial (Na Interface)
Verifique no menu lateral se a API Key foi carregada corretamente (aparecerá "Chave padrão detectada").

Confirme se os PDFs foram listados no "Status do Sistema".

2. Fazendo Perguntas
Digite dúvidas naturais na caixa de texto. Exemplos:

"Quantas horas preciso de CH complementar?"

"Qual o prazo para trancamento de matrícula?"

"O que diz o Art. 15?"

3. Modos de Busca
🔍 Busca Tradicional: Retorna os trechos exatos onde as palavras aparecem, útil para encontrar artigos específicos.

🧠 Perguntar à IA: Lê o contexto das páginas mais relevantes e gera uma resposta explicativa citando as fontes.

4. Dicas
Use as perguntas frequentes (FAQ) no menu lateral para testes rápidos.

Se a IA não souber, ela dirá que não encontrou a informação nos documentos (evitando alucinações).

📁 Estrutura do Projeto

modulo_rag/
├── .streamlit/          # Configurações do Streamlit
├── data/                # Pasta onde ficam os PDFs (Base de conhecimento)
├── venv/                # Ambiente virtual (não versionado)
├── app.py               # Aplicação principal
├── api_key.env          # Chave da API (não versionado)
├── requirements.txt     # Lista de bibliotecas necessárias
└── README.md            # Documentação
