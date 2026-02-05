import pandas as pd

def process_last_gen(last_gen): 
    animal_data_list = []
    for animal in last_gen:
        sia_code = animal['sia_code']

        animal_data = {
            "registration": sia_code[3:5] + sia_code[7:].lstrip("0"),
            "sire_registration": '0',
            "dam_registration": '0',
            "sia_code": sia_code,
            "sire_sia_code": '0',
            "dam_sia_code": '0',  
            "sex": sia_code[6],
            "birth_year": animal['birth_year'],
            "country_id": sia_code[3:5],   
            "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
            "geno": '0'
        }
        
        animal_data_list.append(animal_data)
        
    df = pd.DataFrame(animal_data_list)
    return df