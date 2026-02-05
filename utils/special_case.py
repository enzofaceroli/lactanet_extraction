import logging
import pandas as pd
import httpx
import asyncio

from utils.scraping import scrape_data_limited

async def process_special_case(special_case):    
    print("================= PROCESSING SPECIAL CASE =================")
    special_case_data = []
    animals_to_search = special_case['sia_code']
    
    async with httpx.AsyncClient(timeout=30.0, verify=False) as session:
        tasks = [scrape_data_limited(session, code, True) for code in animals_to_search]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
    for result in results:
        special_case_data.append(result[0])
        
    special_case = pd.DataFrame(special_case_data)    
    logging.info(f"================= FINISHED SPECIAL CASE =================")
    special_case.to_csv('tmp/special_case.csv') 
        
    return special_case