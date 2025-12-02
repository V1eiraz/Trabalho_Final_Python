## 🚌 Sistema de Gerenciamento de Passagens Rodoviárias

Este projeto implementa um sistema de controle de assentos e gestão de linhas para uma empresa de transporte rodoviário de passageiros, desenvolvido em **Python**. O foco é simular o ciclo de vendas, reservas e geração de relatórios de uma frota de ônibus, atendendo a todos os requisitos solicitados pelo professor **Guido**, de Programação em Python.

-----

## ✨ Funcionalidades Principais

O sistema oferece as seguintes funcionalidades :

  * **Cadastro e Gestão de Linhas:** Inclusão, remoção e alteração de rotas (`Origem` -\> `Destino`), horários e valores.
  * **Controle de Assentos:** Cada ônibus suporta **20 assentos** (1-20), onde os **assentos ímpares são nas janelas**. O sistema gerencia a disponibilidade para cada data e linha.
  * **Reservas de Passagens:**
      * Consulta de assentos disponíveis para datas futuras (máximo de **30 dias**).
      * Reserva de assentos individualmente, com registro da venda.
      * **Validação de Partida:** Nenhuma passagem pode ser vendida para ônibus que já partiram (consulta o relógio do sistema).
  * **Carregamento de Reservas via Arquivo (`Reservas.txt`):** Capacidade de ler e processar reservas a partir de um arquivo de texto.
  * **Geração de Relatórios (Tela ou Arquivo):**
      * **Faturamento:** Total arrecadado com venda de passagens no mês corrente, por linha.
      * **Reservas Negadas:** Geração de um arquivo texto (`Reservas_Negadas.txt`) detalhando todas as tentativas de reserva que falharam, juntamente com o motivo (ex.: ônibus cheio, assento ocupado).
  * **Tratamento de Erros:** Verificação de *inputs* do usuário (ex: entrada não numérica, formato de horário/data incorreto).
  * **Estruturas de Dados:** Utilização de **Classes**, **Listas** (vetores), e **Dicionários** conforme exigido.

-----

## ⚙️ Estrutura do Projeto (Classes e Dados)

O código é modularizado para representar as entidades do sistema:

| Classe | Papel no Sistema | Estruturas de Dados Chave |
| :--- | :--- | :--- |
| **`LinhaOnibus`** | O modelo fixo da rota (`Origem`, `Destino`, `Horário`, `Valor`). | Dicionário `onibus_por_data` (chave: `date`, valor: `OnibusDia`). |
| **`OnibusDia`** | Uma instância real do ônibus em uma data específica. | Lista `assentos` (vetor booleano de 20 posições para ocupação). |
| **`SistemaPassagens`** | Gerencia a lógica de negócio, o menu e as coleções de dados. | Listas de `linhas`, `reservas` e `reservas_negadas`. |
| **`Cidade`** | Objeto simples para Origem/Destino. | Lista global `CIDADES`. |

> **Nota:** As mensagens de *print/output* utilizam a biblioteca `colorama` para melhorar a visualização, a clareza e a estética do terminal.

-----

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o **Python 3** instalado.

Este projeto requer as seguintes bibliotecas:

```bash
pip install numpy colorama matplotlib
```

### Passo a Passo

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/V1eiraz/Trabalho_Final_Python.git
    cd Trabalho_Final_Python
    ```

2.  **Crie o arquivo de reservas (`Reservas.txt`):**
  > **Nota:** O arquivo precisa ter exatamente este nome ou não irá funcionar.


3.  
    Crie este arquivo no diretório principal para testar a opção **7** (Ler reservas de arquivo).

    **Conteúdo de `Reservas.txt`**

    ```txt
    divi ; bh ; 19/12/2025 ; 12:00 ; 1
    divi ; bh ; 19/12/2025 ; 12:00 ; 2
    divi ; bh ; 19/12/2025 ; 12:00 ; 3
    divi ; bh ; 19/12/2025 ; 12:00 ; 4
    divi ; bh ; 19/12/2025 ; 12:00 ; 5
    divi ; bh ; 19/12/2025 ; 12:00 ; 6
    divi ; bh ; 19/12/2025 ; 12:00 ; 7
    divi ; bh ; 19/12/2025 ; 12:00 ; 8
    divi ; bh ; 19/12/2025 ; 12:00 ; 9
    divi ; bh ; 19/12/2025 ; 12:00 ; 10
    divi ; bh ; 19/12/2025 ; 12:00 ; 11
    divi ; bh ; 19/12/2025 ; 12:00 ; 12
    divi ; bh ; 19/12/2025 ; 12:00 ; 13
    divi ; bh ; 19/12/2025 ; 12:00 ; 14
    divi ; bh ; 19/12/2025 ; 12:00 ; 15
    divi ; bh ; 19/12/2025 ; 12:00 ; 16
    divi ; bh ; 19/12/2025 ; 12:00 ; 17
    divi ; bh ; 19/12/2025 ; 12:00 ; 18
    divi ; bh ; 19/12/2025 ; 12:00 ; 19
    divi ; bh ; 19/12/2025 ; 12:00 ; 20
    bh ;sp;25/12/2025;09:00; 15
    ```

4.  **Execute o script Python:**

    ```bash
    python3 Trabalho_Final_Python.py
    ```

-----

## 👨‍💻 Autores

Este projeto foi desenvolvido em dupla por:

  * **Davi E. Vieira**
  * **Carlos Daniel Barbosa Silveira**
