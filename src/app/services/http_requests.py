import requests
import re
import time

from logs import log, error
from decompressor import Decompressor

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