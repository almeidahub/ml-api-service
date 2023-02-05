from datetime import datetime


def hoje_data_hora() -> str:
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S')


def log(message:str):
    
    log = f'[{hoje_data_hora()}] INFO: {message}'

    print(log)
    
    
def warning(message:str):
    
    log = f'[{hoje_data_hora()}] WARNING: {message}'

    print(log)
    
    
def error(message:str):
    
    log = f'[{hoje_data_hora()}] ERROR: {message}'

    print(log)