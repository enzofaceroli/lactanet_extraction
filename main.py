import asyncio
import time
import tkinter as tk
from tkinter import filedialog

# Desabilitando avisos causados pelo verify=false
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

from config.logging import setup_logging
setup_logging()

from utils.input_processing import process_input_file
from utils.extraction import data_extraction

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()  # esconde janela principal
    
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo de entrada",
        filetypes=[("Arquivos de texto", "*.txt"), 
                   ("CSV", "*.csv"),
                   ("Todos", "*.*")]
    )
    return caminho
        
 
def main():    
    input_file_path = selecionar_arquivo()
    searched_animals_path = selecionar_arquivo()
    
    if not input_file_path:
        return
    
    start = time.perf_counter()
    animals_to_search, last_gen, special_case, searched_animals = process_input_file(input_file_path, searched_animals_path)
    end = time.perf_counter()

    duration = end - start
    print(f"Time taken to process input flie: {duration:.4f} seconds")

    start = time.perf_counter()
    asyncio.run(data_extraction(animals_to_search, last_gen, special_case, searched_animals, 2))
    end = time.perf_counter()
    
    duration = end - start
    print(f"Time taken to search: {duration:.4f} seconds")
    
if __name__ == '__main__':
    main()
    

