# 🤖 Bot de Download - Dados PEP (Portal da Transparência)

Script Python automatizado para download de dados de **Pessoas Expostas Politicamente (PEP)** do Portal da Transparência do Brasil.

## 📋 Descrição

Este bot realiza o download automático de arquivos `.zip` contendo dados de Pessoas Expostas Politicamente, disponibilizados mensalmente pelo governo brasileiro através do [Portal da Transparência](https://portaldatransparencia.gov.br/download-de-dados/pep).

## 🚀 Instalação e Configuração

### 1. Criar Ambiente Virtual

Abra o terminal na pasta do projeto e execute:

**Windows (PowerShell):**
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\activate
```

**Windows (CMD):**
```cmd
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### 2. Instalar Dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

## 🔧 Como Usar

### Execução Automática

O bot calcula automaticamente o **mês disponível no site** (normalmente 2 meses antes do atual):

```bash
python bot_pep.py
```

**Exemplo**: Se estiver em setembro/2025, baixará julho/2025

O arquivo é automaticamente descompactado após o download.

### Ajuda
```bash
python bot_pep.py --help
```

## 📁 Estrutura de Arquivos

```
bot-requisition-2/
├── bot_pep.py          # Script principal
├── requirements.txt    # Dependências
├── README.md          # Este arquivo
└── downloads/         # Pasta para arquivos baixados
    ├── 202509_PEP.zip
    └── 202509_PEP/    # Pasta criada ao descompactar
        ├── pep.csv
        └── ...
```

## 🎯 Funcionalidades

- ✅ **Download automático** via requisições HTTP
- ✅ **Nome dinâmico** baseado na data atual (formato: `AAAAMM_PEP.zip`)
- ✅ **Headers HTTP** com User-Agent para evitar bloqueios
- ✅ **Tratamento de erros** robusto com mensagens informativas
- ✅ **Progresso visual** durante o download
- ✅ **Descompactação automática** dos arquivos ZIP
- ✅ **Multiplataforma** (Windows, Linux, macOS)
- ✅ **Ambiente isolado** com virtual environment

## ⚠️ Tratamento de Erros

O script inclui tratamento para:

- **Arquivos não encontrados (404)**: Verifica se o arquivo existe para a data solicitada
- **Timeouts de rede**: Configura timeout de 30 segundos para requisições
- **Erros HTTP**: Exibe código e mensagem de erro
- **Arquivos ZIP corrompidos**: Validação antes da descompactação
- **Permissões de arquivo**: Verifica se pode escrever no diretório

## 📊 Exemplo de Saída

```
============================================================
BOT DE DOWNLOAD - DADOS PEP (Portal da Transparência)
============================================================
[INFO] Baixando dados disponíveis: 07/2025
[INFO] Arquivo alvo: 202507_PEP.zip
[INFO] Tentativa 1/3
[INFO] Iniciando download...
[INFO] URL: https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep/202507_PEP.zip
[INFO] Tamanho do arquivo: 2.52 MB
[INFO] Progresso: 100.0%
[SUCESSO] Download concluído: downloads/202507_PEP.zip
[INFO] Descompactando arquivo automaticamente...
[SUCESSO] Arquivos extraídos para: downloads/202507_PEP
============================================================
Processo finalizado!
============================================================
```

## 🔍 URLs e Padrões

- **URL Base**: `https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep`
- **Padrão de arquivo**: `{ano}{mes}_PEP.zip`
- **Exemplo**: `202507_PEP.zip` (julho de 2025 - 2 meses antes do atual)

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas
- **Python 3.7+**
- **requests**: Requisições HTTP
- **zipfile**: Manipulação de arquivos ZIP (built-in)
- **pathlib**: Manipulação de caminhos de arquivo
- **argparse**: Interface de linha de comando

### Testes
Para testar o script:

```bash
# Executar download do mês atual
python bot_pep.py
```

## 📞 Suporte

Se encontrar problemas:
1. Verifique se o ambiente virtual está ativado
2. Confirme que tem conexão com a internet
3. Verifique se a URL está acessível no navegador
4. Consulte as mensagens de erro no console

## 📝 Licença

Este script é open source e está disponível para uso educacional e comercial.

---

**Última atualização**: 15/09/2025 - Bot otimizado para baixar automaticamente o mês disponível no site (2 meses antes do atual)