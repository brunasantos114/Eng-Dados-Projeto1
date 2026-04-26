========== AIRFLOW - CRIAR USUÁRIO ADMIN ==========
 
IMPORTANTE: O usuário admin pode não ser criado automaticamente na primeira execução.
Se receber "Invalid login" ao tentar acessar http://localhost:8080, execute os comandos abaixo:

1. VERIFICAR se o usuário foi criado:
    docker exec -it airflow airflow users list

2. Se não houver usuários, CRIAR o usuário admin:
    docker exec -it airflow airflow users create -u admin -p admin -f admin -l admin -r Admin -e admin@example.com

3. Credenciais padrão para acessar:
    Usuário: admin
    Senha: admin
    URL: http://localhost:8080

OBSERVAÇÃO: Não use essas credenciais em ambientes de produção.

================ PRIMEIRA EXECUÇÃO DO AIRFLOW

Na primeira execução do airflow ocorreram erros e todas as tasks falharam ao rodar a primeira versão. 

Mudanças Realizadas na DAG - postgres_to_minio_csv
Problemas Originais
A primeira versão da DAG tinha vários problemas que faziam as tasks falharem:

Conexão com PostgreSQL falhava - o host "postgres-airflow" não era resolvido corretamente
Cliente S3 estava no escopo global - causava problemas de acesso entre tasks
Funções aninhadas - estavam dentro de um loop, causando confusão de escopo
Objeto S3 não era serializável - o Airflow não conseguia passar o cliente entre tasks usando XCom


Mudanças Implementadas
1. Removeu a task setup_s3_client

O quê: A função que criava o cliente S3 no começo e tentava passar para as outras tasks
Por quê: O boto3 S3 client não é um objeto serializável em JSON, então o Airflow não consegue passar entre tasks
Solução: Agora cada task cria seu próprio cliente S3 dentro dela mesma

2. Criou a function process_table como task independente

O quê: Uma única função que processa uma tabela por vez
Por quê: Simplifica o código e evita problemas de escopo
Solução: Cada tabela (veículos, estados, cidades, etc.) roda em uma task separada e paralela

3. S3 Client agora é criado dentro de cada task

O quê: boto3.client é instanciado dentro da função process_table
Por quê: Cada task é executada isoladamente, então cada uma precisa de sua própria conexão
Solução: Sem necessidade de passar o cliente entre tasks, sem erro de serialização

4. PostgreSQL Hook criado e fechado dentro da task

O quê: Conexão com o banco é aberta, usada e fechada dentro de process_table
Por quê: Evita problemas de conexão aberta/fechada e resolve o erro "could not translate host name"
Solução: Cada execução de task tem sua própria conexão fresca com o banco

5. Removeu a dependência setup >> results

O quê: Tirou a dependência de setup_s3_client rodando primeiro
Por quê: Como removemos a task de setup, não há mais dependência
Solução: Todas as 7 tasks (veículos, estados, cidades, etc.) rodam em paralelo

6. Melhorou o tratamento de erro

O quê: Cada task agora retorna um dicionário com status e informações
Por quê: Facilita identificar qual tabela teve sucesso ou falha
Solução: Logs mais claros e fácil de debugar em caso de problema

7. Estrutura final mais simples

O quê: Uma única função genérica process_table que processa qualquer tabela
Por quê: Código mais limpo, sem repetição
Solução: Lista de tabelas no início, loop que cria tasks para cada uma


Resultado
✅ Todas as 7 tasks rodam com sucesso em paralelo
✅ Dados são extraídos do PostgreSQL sem erro de conexão
✅ CSVs são salvos no MinIO no bucket "landing"
✅ Arquivo max_id.txt é atualizado para cada tabela (para próximas execuções incrementais)
