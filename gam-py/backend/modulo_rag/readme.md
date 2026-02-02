gambot-ufpa/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências
├── .env.example       # Exemplo de configuração
├── data/              # PDFs (não versionado)
└── README.md          # Esta documentação

# Gambot UFPA

**Assistente Acadêmico Inteligente da Universidade Federal do Pará**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

## 📋 Sobre o Projeto

O Gambot UFPA é um sistema inteligente de busca e consulta a documentos acadêmicos da UFPA, combinando busca tradicional com inteligência artificial para fornecer respostas precisas baseadas em regulamentos, grades curriculares e documentos oficiais.

### Funcionalidades

-  **Busca Inteligente** em documentos PDF
-  **Suporte a múltiplos documentos**
-  **Processamento rápido** de grandes volumes de texto
-  **Configuração segura** de API Keys

## Começando

### Pré-requisitos

- Python 3.8+
- Conta na [OpenAI](https://platform.openai.com/) (para API Key)
- Git (opcional)

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/gambot-ufpa.git
   cd gambot-ufpa
   
2. **Crie e ative um ambiente virtual**
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. **Instale as dependências**

bash
pip install -r requirements.txt

4. **Configure as variáveis de ambiente**
   
bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua API Key da OpenAI
# OPENAI_API_KEY=sk-sua_chave_aqui_12345

5. **Adicione seus PDFs**

bash
# Coloque seus arquivos PDF na pasta data/
# Exemplo: copie regulamentos, grades curriculares, etc.

6. **Execute a aplicação**

bash
streamlit run app.py

7. **Acesse no navegador**

text
http://localhost:8501
