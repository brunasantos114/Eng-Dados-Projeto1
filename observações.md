# ========== AIRFLOW - CRIAR USUÁRIO ADMIN ==========
# 
# IMPORTANTE: O usuário admin pode não ser criado automaticamente na primeira execução.
# Se receber "Invalid login" ao tentar acessar http://localhost:8080, execute os comandos abaixo:
#
# 1. VERIFICAR se o usuário foi criado:
#    docker exec -it airflow airflow users list
#
# 2. Se não houver usuários, CRIAR o usuário admin:
#    docker exec -it airflow airflow users create -u admin -p admin -f admin -l admin -r Admin -e admin@example.com
#
# 3. Credenciais padrão para acessar:
#    Usuário: admin
#    Senha: admin
#    URL: http://localhost:8080
#
# OBSERVAÇÃO: Não use essas credenciais em ambientes de produção.