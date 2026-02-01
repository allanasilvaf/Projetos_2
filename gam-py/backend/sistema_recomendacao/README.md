# Sistema de Recomendação de Matérias (UFPA)

Esse é o backend que cuida da lógica de recomendação. Ele lê o histórico do aluno (PDF), processa os dados e sugere as próximas matérias usando KNN (Machine Learning) junto com as regras de pré-requisitos e áreas de conhecimento.

## Estrutura do Projeto

* recomendar_materias.py: O código principal (API Service).
* simulacao_notas.csv: O dataset com notas de veteranos usado para treinar o modelo.
* requirements.txt: Lista das bibliotecas que precisam ser instaladas.

## Como Rodar

### 1. Instalação
Garanta que o Python esteja instalado e rode o comando abaixo para baixar as dependências:

pip install -r requirements.txt

### 2. Como usar no Backend (Flask/FastAPI)

O script foi feito para ser importado como um módulo. A ideia é não alterar o código dele, apenas chamar as funções onde for necessário.

A. Upload do Histórico
Quando o usuário enviar o PDF, salve o arquivo temporariamente e chame a função assim:

import recomendar_materias

# aluno_id: Inteiro ou String que identifica o usuário logado
# caminho_pdf: Caminho do arquivo salvo no servidor
resultado = recomendar_materias.processar_upload_pdf("temp_historico.pdf", aluno_id=1)

print(resultado)
# Retorna algo como: {'status': 'success', 'mensagem': 'Histórico processado', 'materias_lidas': 45}

B. Gerar Recomendação
Para pegar os dados e exibir no Frontend, chame esta função que já devolve o JSON pronto:

dados_frontend = recomendar_materias.obter_recomendacao_json(aluno_id=1)

O JSON de retorno segue essa estrutura:

{
  "status": "success",
  "diagnostico_competencias": {
    "EXATAS": { "media": 4.5, "status": "Dificuldade" },
    "SOFTWARE": { "media": 8.0, "status": "OK" }
  },
  "lista_prioridade": [
    {
      "codigo": "EC01006",
      "nome": "CALCULO II",
      "score": 0.95,
      "aviso": "ALERTA_DIFICULDADE" // Aparece se a média da área for baixa
    }
  ],
  "lista_flexivel": [ ... ]
}

## Importante

1. Dataset: O arquivo simulacao_notas.csv precisa estar na mesma pasta do script recomendar_materias.py no servidor, senão o modelo não tem base para rodar.
2. Banco de Dados: O sistema cria automaticamente arquivos .db locais (dataset_geral.db e aluno_logado.db). Verifique se a pasta tem permissão de escrita.
