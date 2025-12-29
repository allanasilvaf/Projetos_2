# 🚀 Instalação Rápida - GAM.py

## 📋 Pré-requisitos
Antes de começar, instale:
- [Node.js](https://nodejs.org/) (versão 16+)
- [PHP](https://www.php.net/) (versão 7.4+)
- [MySQL](https://www.mysql.com/) ou MariaDB


  
## 📐Estrutura dos Arquivos

```
📦 gam-py/
├── 🗄️ backend/                       # Servidor backend em PHP
│   ├── 🔌 api/                      # Endpoints da API REST
│   ├── 🧩 classes/                  # Classes PHP (Models, Controllers)
│   ├── ⚙️ config/                   # Configurações (banco de dados, etc.)
│   ├── 🚀 index.php                 # Ponto de entrada principal
│   ├── 🌱 seed.php                  # Popula banco com dados iniciais
│   └── 🔧 test_connection.php       # Testa conexão com banco
└── 🎨 frontend/                     # Aplicação frontend Vue.js
    ├── 📄 app.js                    # Entry point da aplicação
    ├── 🖼️ assets/                   # Imagens, ícones, fonts
    ├── 📦 dist/                     # Build de produção (npm run build)
    ├── 📚 node_modules/             # Dependências (não commit)
    ├── 🌐 public/                   # Arquivos estáticos públicos
    ├── 📝 src/                      # Código fonte principal
    │   ├── 🧱 components/           # Componentes reutilizáveis
    │   ├── 🖥️ views/                # Páginas da aplicação
    │   ├── 🛣️ router/               # Configuração de rotas
    │   ├── 🗃️ store/                # Gerenciamento de estado
    │   └── ⚡ main.js               # Inicialização do Vue
    ├── 🔧 .browserslistrc           # Compatibilidade com navegadores
    ├── 🧹 .eslintrc.js              # Regras de linting
    ├── 🔒 .gitignore                # Ignora arquivos no Git
    ├── ⚡ babel.config.js           # Transpilação JavaScript
    ├── 📋 jsonfig.json              # Configuração JSON (typ: jsconfig.json)
    ├── 📦 package-lock.json         # Lock de dependências
    ├── 📦 package.json              # Dependências e scripts
    ├── 📖 README.md                 # Documentação
    └── ⚙️ vue.config.js             # Configuração Vue CLI
```


## 🛠️ Passo a Passo

### 1. Clone o repositório

```bash
git clone https://github.com/allanasilvaf/Projetos_2.git
cd Projetos_2
```


### 2. Configure o frontend Vue.js

```bash
# Instale as dependências
npm install 
```
```bash
# Instale as dependências
npm run serve
```
```bash
# Em um novo terminal, volte na pasta frontend para iniciar a produção.
npm run build
```

### 3. Inicie o Banco de dados
```bash
# Em um novo terminal, entre na pasta backend
php seed.php
```
 
### 4. Acesse o sistema
```bash 
🌐 URL do frontend: http://localhost:8080

🔧 URL da API: http://localhost:8000/api/
```
  