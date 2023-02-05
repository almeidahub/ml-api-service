import requests
import shutil
import re
import gzip
import os
import time
from logs import log, error


class HttpRequests():
    """Classe para fazer download de arquivos da web."""

    @staticmethod
    def download(url, compression=None):
        """Baixa um arquivo da web.

        Args:
            url (str): A URL do arquivo a ser baixado.
            compression (str, optional): O tipo de compressão, se houver. Padrão é None.

        Returns:
            str: O nome do arquivo baixado.
        """ 
        
        # Verifica se a URL é válida
        if not url:
            raise ValueError("URL inválida")

        # Gera o nome do arquivo a partir da URL
        file_name = re.split(pattern='/', string=url)[-1]
        
        # Adiciona um timestamp para evitar sobrescrever arquivos
        file_name = f"{int(time.time())}_{file_name}"

        log(f'Baixando de {url}...')
        
        # Tenta fazer o download do arquivo
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(file_name, 'wb') as f:
                f.write(response.content)
                
        except requests.exceptions.RequestException as e:
            error(f"Erro ao baixar arquivo: {e}")
            raise
        
        # Verifica se há compressão
        if compression == 'gzip':
            Decompressor.decompress_gzip(file_name)
                    
        return file_name
    

class Decompressor():
    """Classe para descompactar arquivos."""

    @staticmethod
    def decompress_gzip(file_name: str, remove_old: bool = True) -> str:
        """Descompacta um arquivo GZIP.

        Args:
            file_name (str): O nome do arquivo GZIP a ser descompactado.
            remove_old (bool, optional): Se deve remover o arquivo original após a descompressão. Padrão é True.

        Returns:
            str: O nome do arquivo descompactado.
        """
        
        # Verifica se o arquivo de entrada existe
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_name}")

        # Gera o nome do arquivo de saída
        file_name_out = file_name.replace('.gz', '')

        # Verifica se o arquivo de saída já existe
        if os.path.exists(file_name_out):
            raise FileExistsError(f"Arquivo já existe: {file_name_out}")
        
        log(f'Descompactando arquivo gzip {file_name} para {file_name_out}')

        # Tenta descompactar o arquivo
        try:
            with gzip.open(file_name, 'rb') as f_in:
                with open(file_name_out, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            error(f"Erro ao descompactar arquivo: {e}")
            raise

        # Remove o arquivo original se especificado
        if remove_old:
            os.remove(file_name)
            
        return file_name_out
