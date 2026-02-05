import pandas as pd
import time
import httpx
import asyncio

from utils.utils import sia_code_to_registration
from utils.scraping import scrape_data_limited
from utils.special_case import process_special_case
from utils.last_gen import process_last_gen

async def data_extraction(animals_to_search, last_gen, special_case, searched_animals, max_generation):
    generation = 0
    searched_animals_data = []
    next_gen = []   
    
    start = time.perf_counter()
    special_case_df = await process_special_case(special_case)
    end = time.perf_counter()
    
    duration = end - start
    print(f"Time taken to process special case: {duration:.4f} seconds")
    
    set_special_case = set(special_case_df)
    
    if (set_special_case):
        searched_animals = searched_animals | set(special_case_df['registration'])
    
    while not animals_to_search.empty: 
        print(f"==================== STARTING GEN {generation} ====================")
        async with httpx.AsyncClient(timeout=30.0, verify=False) as session:
            tasks = [
                scrape_data_limited(session, code, False) 
                for code in animals_to_search
                if code not in searched_animals
                ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
                    
        for result in results:
            if isinstance(result, Exception):
                continue
            
            animal_data, sire_dict, dam_dict = result
            
            searched_animals.add(animal_data['registration'])
            searched_animals_data.append(animal_data)  

            if sire_dict is not None:
                sire_registration = sia_code_to_registration(sire_dict["sia_code"])
                if generation == max_generation - 1 or int(animal_data['birth_year']) < 1990:
                    if(sire_registration not in searched_animals):
                        last_gen.append(sire_dict)
                        searched_animals.add(sire_registration)

                else:
                    if(sire_registration not in searched_animals):
                        next_gen.append(sire_dict["sia_code"])
                        
            if dam_dict is not None:
                dam_registration = sia_code_to_registration(dam_dict["sia_code"])
                if generation == max_generation - 1 or int(animal_data['birth_year']) < 1990:
                    if(dam_registration not in searched_animals):
                        last_gen.append(dam_dict)
                        searched_animals.add(dam_registration)
                    
                else:
                    if(dam_registration not in searched_animals):
                        next_gen.append(dam_dict['sia_code'])
                    
        # evita duplicatas
        next_gen = [code for code in set(next_gen) if code not in searched_animals]
        next_gen = list(set(next_gen))  
                
        animals_to_search = pd.Series(next_gen)
        next_gen = []
        generation += 1
        
    data = pd.DataFrame(searched_animals_data)
    final_df = pd.concat([special_case_df, data])
    final_df = pd.concat([final_df, process_last_gen(last_gen)]).drop_duplicates(subset=["sia_code"])
    
    final_df.to_csv('tmp/data.csv', index=False)