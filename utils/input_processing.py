import logging
import pandas as pd
import numpy as np

def process_input_file(input_file_path, searched_animals_path):
    print("================= PROCESSING INPUT FILE =================")

    columns = ["registration", "sia_code", "sex", "birth_year", "country1", "country2"]
    df = pd.read_csv(input_file_path, names=columns, dtype=str)
    
    cols = ['registration']
    searched_animals = pd.read_csv(searched_animals_path, names=cols)
    searched_animals = set(searched_animals["registration"])
    
    incomplete_line_mask = df["birth_year"].isnull()
    
    # Resolvendo o problema das vacas que não tem o sexo no seu registro
    processed_df = pd.DataFrame()
    processed_df['registration'] = df['registration']
    processed_df['sia_code'] = df['sia_code']

    processed_df['sex'] = np.where(incomplete_line_mask, 'F', df["sex"])
    processed_df['country1'] = np.where(incomplete_line_mask, df["sex"], df["country1"])
    processed_df['country2'] = np.where(incomplete_line_mask, df["country1"], df["country2"])
    processed_df['birth_year'] = np.where(incomplete_line_mask, df["country2"], df["birth_year"])
    # ===================================================================================
    
    df = processed_df.copy()
    
    searched_mask = df['registration'].isin(searched_animals)
    df = df[~searched_mask]

    df["birth_year"] = pd.to_numeric(df["birth_year"], errors='coerce')       
     
    special_case = df[df["birth_year"] == 1911]    

    df = df.drop(["registration", "country1", "country2", "sex"], axis=1)
    
    last_gen = df[(df["birth_year"] <= 1990) & (df["birth_year"] != 1911)].to_dict(orient='records')
    search = df[df["birth_year"] > 1990]
    search = search['sia_code']
    
    # retornar lista de animais a serem buscados
    # retornar lista de animais de ultima geração (não serão buscados)  
    # retornar caso especial (será buscado apenas a data de nascimento do animal)
    logging.info(f"================= FINISHED INPUT FILE =================")
    print(f"Amount of animals to search: {len(search)}\n")
    print(f"Amount of animals in last gen: {len(last_gen)}\n")
    print(f"Amount of animals in special_case: {len(special_case)}\n")
    print(f"Amount of animals searched: {len(searched_animals)}\n\n")

    return search, last_gen, special_case, searched_animals 