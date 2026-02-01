# 🚀 Instalação Rápida - GAM.py

  
## 📐Estrutura dos Arquivos

```
📦 gam-py/
├── 🐳 docker-compose.yml           # Orquestração dos containers
├── 🗄️ backend/                    # Servidor backend em PHP
│   ├── 🐳 Dockerfile              # Imagem Docker do backend
│   ├── 🔌 api/                    # Endpoints da API REST
│   ├── 🧩 classes/                # Classes PHP (Models, Controllers)
│   ├── ⚙️ config/                 # Configurações (banco de dados, etc.)
│   ├── 🚀 index.php               # Ponto de entrada principal
│   ├── 🌱 seed.php                # Popula banco com dados iniciais
│   └── 🔧 test_connection.php     # Testa conexão com banco
├── 🎨 frontend/                   # Aplicação frontend Vue.js
│   ├── 📄 app.js                  # Entry point da aplicação
│   ├── 🖼️ assets/                 # Imagens, ícones, fonts
│   ├── 📦 dist/                   # Build de produção (npm run build)
│   ├── 📚 node_modules/           # Dependências (não commit)
│   ├── 🌐 public/                 # Arquivos estáticos públicos
│   ├── 📝 src/                    # Código fonte principal
│   │   ├── 🧱 components/         # Componentes reutilizáveis
│   │   ├── 🖥️ views/              # Páginas da aplicação
│   │   ├── 🛣️ router/             # Configuração de rotas
│   │   ├── 🗃️ store/              # Gerenciamento de estado
│   │   └── ⚡ main.js             # Inicialização do Vue
│   ├── 🔧 .browserslistrc         # Compatibilidade com navegadores
│   ├── 🧹 .eslintrc.js            # Regras de linting
│   ├── 🔒 .gitignore              # Ignora arquivos no Git
│   ├── ⚡ babel.config.js         # Transpilação JavaScript
│   ├── 📋 jsconfig.json           # Configuração JavaScript
│   ├── 📦 package-lock.json       # Lock de dependências
│   ├── 📦 package.json            # Dependências e scripts
│   ├── 📖 README.md               # Documentação do frontend
│   └── ⚙️ vue.config.js           # Configuração Vue CLI
├── 🗃️ init.sql                   # Script de inicialização do banco MySQL
└── 📖 README.md                   
```


## 🛠️ Passo a Passo

### 🐳 GAM-PY - Execução com Docker

## Pré-requisitos
- Docker e Docker Compose instalados

## 🚀 Iniciar o projeto
```bash
git clone https://github.com/seu-usuario/gam-py.git


```bash
# Em um terminal, vá para o endereço do arquivo
cd gam-py
```
```bash
# Digite o comando:
docker-compose up -d
```

### Acessos:
🌐 http://localhost:5174    # Frontend Vue
⚙️  http://localhost:9000    # Backend PHP  
🗄️  http://localhost:8080    # phpMyAdmin

