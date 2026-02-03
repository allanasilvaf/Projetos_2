# GAMBOT 

**Assistente Acadêmico Inteligente da Universidade Federal do Pará**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

## Sobre o Projeto

O **Gambot UFPA** é um sistema inteligente de busca e consulta a documentos acadêmicos da UFPA. Ele combina:

-  **Busca tradicional** por palavras-chave em PDFs
-  **Inteligência Artificial** para respostas contextualizadas
-  **Base de conhecimento** em regulamentos e documentos oficiais
-  **Sistema híbrido** que usa o melhor de ambas as abordagens

###  Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|-----------|
| **Busca Inteligente** | Expande automaticamente termos com sinônimos |
| **IA Contextual** | Respostas baseadas no conteúdo dos documentos |
| **Controle de Fontes** | Sempre mostra de qual documento veio a informação |

## Começando Rápido

### Pré-requisitos

- Python 3.8 ou superior
- Conta na [OpenAI](https://platform.openai.com/) (para API Key)
- PDFs com regulamentos/grade curricular da UFPA

### Instalação Passo a Passo

1. **Clone o repositório**
   git clone https://github.com/allanasilvaf/gam-py.git
   cd modulo_rag
   
Instale as dependências

pip install -r requirements.txt
Configure a API Key

Crie um arquivo api_key.env na pasta principal

Adicione: OPENAI_API_KEY=sua_chave_aqui

⚙️ Configuração
Crie um arquivo api_key.env com:

env
OPENAI_API_KEY=sua_chave_aqui_123456

Adicione seus PDFs

Coloque seus arquivos PDF desejados na pasta data/

Execute o sistema

streamlit run app.py
Acesse no navegador

text
http://localhost:8501

🎮 Como Usar (já na interface)
1. Configuração Inicial
Configure sua API Key no menu lateral

Ative/desative a IA conforme necessário

Verifique se os PDFs foram carregados

2. Fazendo Perguntas
Digite perguntas como:

"disciplinas do 6º período"

"Como funciona o trancamento de matrícula?"

"Qual é a carga horária total do curso?"

"Art. 15"

3. Tipos de Busca
Busca Tradicional (🔍): Mostra trechos dos documentos

Perguntar à IA (🧠): Resposta inteligente e contextual

4. FAQ Rápido
Use as perguntas frequentes no menu lateral para começar rápido!

📁 Estrutura do Projeto
gambot-ufpa/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── README.md           # Esta documentação
├── .gitignore          # Arquivos ignorados no Git
├── .env.example        # Exemplo de configuração
└── data/               # Pasta para PDFs
    └── .gitkeep        # Mantém a pasta no Git
    
