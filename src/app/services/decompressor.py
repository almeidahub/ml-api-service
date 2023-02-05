import shutil
import gzip
import os
from logs import log, error

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