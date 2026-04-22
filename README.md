# 🚀 Projeto de Engenharia de Dados — Pipeline com Airflow, Spark, dbt e Metabase

## 📌 Visão Geral

Este projeto tem como objetivo construir um pipeline de dados moderno utilizando ferramentas amplamente adotadas no mercado, seguindo uma arquitetura de **Data Lake + Data Warehouse**.
Neste momento, o foco do projeto não está na aplicação de regras de negócio, mas sim na familiarização com o fluxo e a integração entre as ferramentas utilizadas.
A solução contempla desde a ingestão de dados até a camada de consumo para análise.

---

## 🏗️ Arquitetura

A arquitetura do projeto está organizada nas seguintes camadas:

<img width="962" height="365" alt="image" src="https://github.com/user-attachments/assets/d7abdd27-f202-4688-b6ae-2cbd63c6e784" />


### 🔄 Fluxo de Dados

1. Dados são coletados de diferentes fontes (APIs, arquivos, bancos)
2. O **Apache Spark** realiza o processamento inicial
3. Os dados são armazenados em um **Data Lake (camada Landing)**
4. O **dbt** transforma os dados em:
   * Dimensões
   * Fatos
5. Os dados tratados são carregados no **Data Warehouse (MariaDB)**
6. O **Metabase** consome os dados para visualização

---

## 🧰 Tecnologias Utilizadas

* **Apache Airflow** → Orquestração de pipelines
* **Apache Spark** → Processamento distribuído
* **dbt** → Transformação de dados
* **MariaDB** → Data Warehouse
* **Metabase** → Visualização de dados
* **Docker & Docker Compose** → Containerização

---

## 📁 Estrutura do Projeto

```bash
.
├── airflow/
│   ├── dags/
│   └── config_airflow/
├── spark_connector/
│   └── read_data.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

## ⚙️ Status Atual do Projeto

🚧 **Em desenvolvimento**

Atualmente, foram implementados:

* [x] Estrutura inicial do projeto
* [x] Configuração do ambiente com Docker
* [x] Subida dos serviços:

  * Airflow
  * Spark
  * MariaDB
  * Metabase

Próximos passos:

* [ ] Implementar ingestão de dados (Spark)
* [ ] Criar DAGs no Airflow
* [ ] Modelagem com dbt
* [ ] Integração com Data Warehouse
* [ ] Construção de dashboards no Metabase

---

## 📊 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:

* Prática de engenharia de dados moderna
* Simulação de pipeline real de dados
* Uso de boas práticas de mercado
* Construção de portfólio profissional

---
