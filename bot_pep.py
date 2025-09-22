#!/usr/bin/env python3
"""
Bot de Download Automático - Dados PEP (Pessoas Expostas Politicamente)
Portal da Transparência do Brasil

Este script realiza o download automático dos dados de Pessoas Expostas Politicamente
no formato ZIP através de requisições HTTP diretas.

Autor: Bot de Transparência
Data: 15/09/2025
"""

import os
import sys
import requests
import zipfile
from datetime import datetime
from pathlib import Path
import argparse


class BotPEPDownload:
    """
    Classe responsável pelo download e gerenciamento de arquivos PEP
    """
    
    def __init__(self):
        self.base_url = "https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/pep"
        self.download_dir = Path("downloads")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        # Criar diretório de downloads se não existir
        self.download_dir.mkdir(exist_ok=True)
    
    def gerar_nome_arquivo(self, data_ref=None):
        """
        Gera o nome do arquivo baseado na data atual ou data fornecida
        
        Args:
            data_ref (datetime): Data de referência. Se None, usa data atual
            
        Returns:
            str: Nome do arquivo no formato AAAAMM_PEP.zip
        """
        if data_ref is None:
            data_ref = datetime.now()
        
        ano_mes = data_ref.strftime("%Y%m")
        return f"{ano_mes}_PEP.zip"
    
    def construir_url_download(self, data_ref=None):
        """
        Constrói a URL completa para download
        
        Args:
            data_ref (datetime): Data de referência
            
        Returns:
            str: URL completa para download
        """
        nome_arquivo = self.gerar_nome_arquivo(data_ref)
        return f"{self.base_url}/{nome_arquivo}"
    
    def baixar_arquivo(self, url, nome_arquivo):
        """
        Realiza o download do arquivo com retry automático
        
        Args:
            url (str): URL do arquivo
            nome_arquivo (str): Nome do arquivo a ser salvo
            
        Returns:
            bool: True se download bem-sucedido, False caso contrário
        """
        import time
        
        caminho_arquivo = self.download_dir / nome_arquivo
        
        # Configurações de retry
        max_tentativas = 3
        tentativa = 1
        
        while tentativa <= max_tentativas:
            print(f"[INFO] Tentativa {tentativa}/{max_tentativas}")
            print(f"[INFO] Iniciando download...")
            print(f"[INFO] URL: {url}")
            
            try:
                response = requests.get(url, headers=self.headers, stream=True, timeout=30)
                
                # Verificar se é um erro 403 (pode ser temporário)
                if response.status_code == 403:
                    print(f"[AVISO] Acesso temporariamente bloqueado (403)")
                    if tentativa < max_tentativas:
                        print(f"[INFO] Aguardando 2 segundos antes de tentar novamente...")
                        time.sleep(2)
                        tentativa += 1
                        continue
                
                response.raise_for_status()
                
                # Verificar se é realmente um arquivo ZIP
                content_type = response.headers.get('content-type', '')
                if 'zip' not in content_type.lower() and 'octet-stream' not in content_type.lower():
                    print(f"[ERRO] Tipo de conteúdo inesperado: {content_type}")
                    return False
                
                # Obter tamanho do arquivo
                tamanho_total = int(response.headers.get('content-length', 0))
                
                print(f"[INFO] Tamanho do arquivo: {tamanho_total / (1024*1024):.2f} MB")
                
                # Download com barra de progresso simples
                with open(caminho_arquivo, 'wb') as f:
                    baixado = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            baixado += len(chunk)
                            
                            # Atualizar progresso
                            if tamanho_total > 0:
                                progresso = (baixado / tamanho_total) * 100
                                print(f"\r[INFO] Progresso: {progresso:.1f}%", end="", flush=True)
                
                print(f"\n[SUCESSO] Download concluído: {caminho_arquivo}")
                return True
                
            except requests.exceptions.Timeout:
                print(f"[ERRO] Timeout ao tentar baixar o arquivo")
                if tentativa < max_tentativas:
                    print(f"[INFO] Tentando novamente...")
                    tentativa += 1
                    continue
                return False
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"[ERRO] Arquivo não encontrado: {nome_arquivo}")
                    print(f"[INFO] Verifique se a data está correta ou tente outro mês")
                elif e.response.status_code == 403:
                    print(f"[ERRO] Acesso negado (403). O servidor pode estar bloqueando downloads automáticos.")
                    print(f"[INFO] Tente acessar o arquivo manualmente no navegador primeiro.")
                else:
                    print(f"[ERRO] Erro HTTP {e.response.status_code}: {e}")
                return False
                
            except Exception as e:
                print(f"[ERRO] Erro durante o download: {str(e)}")
                if tentativa < max_tentativas:
                    print(f"[INFO] Tentando novamente...")
                    tentativa += 1
                    continue
                return False
            
            tentativa += 1
        
        return False
    
    def descompactar_arquivo(self, nome_arquivo):
        """
        Descompacta o arquivo ZIP baixado
        
        Args:
            nome_arquivo (str): Nome do arquivo ZIP
            
        Returns:
            bool: True se descompactação bem-sucedida, False caso contrário
        """
        caminho_arquivo = self.download_dir / nome_arquivo
        
        if not caminho_arquivo.exists():
            print(f"[ERRO] Arquivo não encontrado: {caminho_arquivo}")
            return False
        
        try:
            # Criar pasta para extrair arquivos
            nome_pasta = nome_arquivo.replace('.zip', '')
            pasta_extracao = self.download_dir / nome_pasta
            pasta_extracao.mkdir(exist_ok=True)
            
            print(f"[INFO] Descompactando arquivo...")
            
            with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                # Listar arquivos no ZIP
                arquivos = zip_ref.namelist()
                print(f"[INFO] Arquivos encontrados: {len(arquivos)}")
                
                # Extrair todos os arquivos
                zip_ref.extractall(pasta_extracao)
                
                # Listar arquivos extraídos
                print("[INFO] Arquivos extraídos:")
                for arquivo in arquivos:
                    print(f"  - {arquivo}")
            
            print(f"[SUCESSO] Arquivos extraídos para: {pasta_extracao}")
            return True
            
        except zipfile.BadZipFile:
            print(f"[ERRO] Arquivo ZIP corrompido ou inválido")
            return False
        except Exception as e:
            print(f"[ERRO] Erro ao descompactar: {str(e)}")
            return False
    
    def detectar_mes_disponivel(self):
        """
        Detecta automaticamente o mês mais recente disponível no site
        
        Returns:
            datetime: Data do mês disponível mais recente, ou None se não encontrar
        """
        print("[INFO] Detectando mês disponível automaticamente...")
        
        # Começar do mês atual e voltar até 6 meses
        hoje = datetime.now()
        
        for meses_atras in range(0, 6):  # Tentar até 6 meses atrás
            if hoje.month - meses_atras <= 0:
                # Se ultrapassar janeiro, voltar para o ano anterior
                ano = hoje.year - 1
                mes = 12 + (hoje.month - meses_atras)
            else:
                ano = hoje.year
                mes = hoje.month - meses_atras
            
            # Testar se o arquivo existe para este mês
            data_teste = datetime(ano, mes, 1)
            nome_arquivo_teste = self.gerar_nome_arquivo(data_teste)
            url_teste = self.construir_url_download(data_teste)
            
            print(f"[INFO] Testando mês: {data_teste.strftime('%m/%Y')}")
            
            try:
                # Fazer uma requisição HEAD para verificar se o arquivo existe
                response = requests.head(url_teste, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    # Verificar se é um arquivo ZIP válido
                    content_type = response.headers.get('content-type', '')
                    content_length = int(response.headers.get('content-length', 0))
                    
                    if ('zip' in content_type.lower() or 'octet-stream' in content_type.lower()) and content_length > 0:
                        print(f"[SUCESSO] Mês disponível encontrado: {data_teste.strftime('%m/%Y')}")
                        return data_teste
                        
            except requests.exceptions.RequestException:
                # Se houver erro de conexão, continuar tentando
                continue
        
        print("[ERRO] Não foi possível detectar nenhum mês disponível nos últimos 6 meses")
        return None

    def executar(self, descompactar=False, data_ref=None):
        """
        Executa o processo completo de download
        
        Args:
            descompactar (bool): Parâmetro mantido para compatibilidade (descompactação é automática)
            data_ref (datetime): Data de referência para o arquivo. Se None, detecta automaticamente
        """
        print("=" * 60)
        print("BOT DE DOWNLOAD - DADOS PEP (Portal da Transparência)")
        print("=" * 60)
        
        # Se não foi fornecida data de referência, detectar automaticamente
        if data_ref is None:
            data_ref = self.detectar_mes_disponivel()
            if data_ref is None:
                print("[ERRO] Não foi possível detectar o mês disponível automaticamente")
                print("[INFO] Tentando com mês padrão (2 meses atrás)...")
                # Fallback para o método original
                hoje = datetime.now()
                if hoje.month <= 2:
                    ano = hoje.year - 1
                    mes = hoje.month + 10
                else:
                    ano = hoje.year
                    mes = hoje.month - 2
                data_ref = datetime(ano, mes, 1)
        
        # Gerar nome do arquivo e URL
        nome_arquivo = self.gerar_nome_arquivo(data_ref)
        url = self.construir_url_download(data_ref)
        
        print(f"[INFO] Baixando dados disponíveis: {data_ref.strftime('%m/%Y')}")
        print(f"[INFO] Arquivo alvo: {nome_arquivo}")
        
        # Realizar download
        sucesso = self.baixar_arquivo(url, nome_arquivo)
        
        # Descompactar automaticamente após download
        if sucesso:
            print("[INFO] Descompactando arquivo automaticamente...")
            self.descompactar_arquivo(nome_arquivo)
        
        print("=" * 60)
        print("Processo finalizado!")
        print("=" * 60)


def main():
    """
    Função principal - ponto de entrada do script
    """
    parser = argparse.ArgumentParser(
        description="Bot de download automático de dados PEP do Portal da Transparência"
    )
    
    parser.add_argument(
        "--descompactar", 
        action="store_true",
        help="Descompactar o arquivo ZIP após download (descompactação automática por padrão)"
    )
    
    parser.add_argument(
        "--mes-fixo", 
        action="store_true",
        help="Usar lógica fixa de 2 meses atrás (desativa detecção automática)"
    )
    
    args = parser.parse_args()
    
    # Criar instância do bot
    bot = BotPEPDownload()
    
    if args.mes_fixo:
        # Usar lógica fixa original (2 meses atrás)
        hoje = datetime.now()
        if hoje.month <= 2:
            ano = hoje.year - 1
            mes = hoje.month + 10
        else:
            ano = hoje.year
            mes = hoje.month - 2
        data_ref = datetime(ano, mes, 1)
        bot.executar(descompactar=args.descompactar, data_ref=data_ref)
    else:
        # Usar detecção automática (padrão)
        print("[INFO] Usando detecção automática do mês disponível...")
        bot.executar(descompactar=args.descompactar, data_ref=None)


if __name__ == "__main__":
    main()