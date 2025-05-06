**Script de Download, Extração e Agendamento de Arquivos SICONV**

O script automatiza o processo de download, verificação de integridade, extração e registro de data de carga de arquivos CSV compactados do portal de dados do governo federal http://repositorio.dados.gov.br/seges/detru/ (SICONV).
Também permite o agendamento automático dessas tarefas em horários específicos.

**Baixa os arquivos .zip de URLs predefinidas.**

         "http://repositorio.dados.gov.br/seges/detru/siconv_convenio.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_empenho.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_emenda.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_programa.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_programa_proposta.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_desembolso.csv.zip",
        "http://repositorio.dados.gov.br/seges/detru/siconv_proposta.csv.zip"

Verifica a integridade do arquivo ZIP antes de extraí-lo > Extrai arquivos ZIP para uma pasta local > Exemplo: folder = r"C:\dados"

Registra a data de modificação do arquivo siconv_proposta.csv em um arquivo CSV auxiliar.

Agenda a execução automática da tarefa diariamente às 07:00 e 13:30.

**Requisitos:**

Python 3.6+
Bibliotecas: requests, schedule

**Para instação da bibliotecas**

>> pip install requests schedule

**Estrutura do Código**

download_and_extract(url, folder): Gerencia o download e extração de arquivos, com verificação de integridade.

write_data_carga_csv(folder, file_name): Cria um CSV com a data atual e a data de modificação dos arquivos

job(): Executa o processo completo para todos os arquivos da lista de URLs.

schedule_jobs(): Agenda os horários de execução automática.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
**Conteúdo do Arquivo .pbix

Conexões com fontes de dados externas (CSV), Tratamento e transformação de dados via Power Query, Modelagem de dados (relacionamentos, colunas calculadas, medidas DAX), Relatórios com visuais interativos e segmentações, Filtros por UF, Ano do instrumento, convenente  entre outros.

**Requisitos para Utilização:**

Microsoft Power BI Desktop
Conexão com a Fonte de Dados 
Power BI Gateway (Pessoal ou Corporativo)
Necessário para agendar a atualização de dados quando o relatório for publicado no Power BI Service.

**Como Usar**

Abra o arquivo .pbix com o Power BI Desktop.
Vá até a aba Página Inicial > Atualizar. (Caso seja necessário ajustar o caminho de algum arquivo CSV ou pasta, clique em Transformar Dados > Fonte e modifique os caminhos conforme necessário)

**PUBLICAÇÃO**

Publique no Power BI Service para comPartilhamento on line.

**Publicação e Atualização Automática com Gateway**

1. Publicar no Power BI Service
Clique em Publicar no Power BI Desktop.
Escolha o workspace desejado (Meu workspace).
2. Instalar e Configurar o Gateway
Baixe o gateway:
https://powerbi.microsoft.com/pt-br/gateway/
Instale como Gateway Pessoal (uso individual) ou Gateway Padrão (Corporativo) se for multiusuário.
Após instalar, conecte à sua conta Microsoft e mantenha o gateway sempre em execução no computador ou servidor onde os arquivos estão salvos.

**Configurar a Atualização Agendada**

Acesse https://app.powerbi.com e vá até o workspace onde o relatório foi publicado.
Clique nos três pontos (...) > Configurações ao lado do dataset.
Em "Gateway de dados", selecione o gateway configurado.
Em "Credenciais de fonte de dados", insira as credenciais de acesso aos arquivos locais (ex: Windows).
Vá em Agendamento de atualização > Marque para manter atualizado > Defina os horários desejados (ex: 07:00 e 13:30) > Salve.

Caso haja erros de atualização, verifique: Se o caminho dos arquivos locais está correto, se os nomes das colunas ou arquivos mudaram e se há permissões de leitura adequadas.






