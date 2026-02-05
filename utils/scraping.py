import httpx
from bs4 import BeautifulSoup
import asyncio
import logging
from datetime import datetime

from utils.utils import sia_code_to_url, sia_code_to_registration, convert_birth_year, url_to_animal_data

MAX_CONCURRENT = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

async def scrape_data(session: httpx.AsyncClient, sia_code:str, special_case:bool):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Referer": "https://lactanetgen.ca/query/query-individual.php",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    
    url = sia_code_to_url(sia_code)
    registration = sia_code_to_registration(sia_code)
    
    try:
        response = await session.get(url, headers=headers, timeout=15.0)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if special_case:
                birth_date = soup.select_one("div.col-5 span.Stat").string

                birth_year = convert_birth_year(birth_date[25:27])
                
                animal_data = {
                    "registration": registration,
                    "sire_registration": '0',
                    "dam_registration": '0',
                    "sia_code": sia_code,
                    "sire_sia_code": '0',
                    "dam_sia_code": '0',  
                    "sex": sia_code[6],
                    "birth_year": birth_year,
                    "country_id": sia_code[3:5],   
                    "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
                    "geno": '0'
                }
            
                return animal_data, None, None
            
            logging.info(f"SCRAPING FOR {sia_code} SUCCESSFUL")
            
            sire_tag = soup.find("span", class_="RegistrationLabel", string="Sire:").find_next("a")
            dam_tag = soup.find("span", class_="RegistrationLabel", string="Dam:").find_next("a")      
            
            birth_date = soup.select_one("div.col-5 span.Stat").string
            
            current_year = datetime.now().year % 1000

            birth_year = int(birth_date[25:27])
            birth_year = (2000 + birth_year) if birth_year < current_year else (1900 + birth_year)
                
            base_url = "https://lactanetgen.ca/query/"
            sire_url = base_url + sire_tag["href"].replace('®', '&reg')
            dam_url = base_url + dam_tag["href"].replace('®', '&reg')  
            
            sire_sia_code, sire_registration = url_to_animal_data(sire_url)     
            dam_sia_code, dam_registration = url_to_animal_data(dam_url)    
            
            parent_birth_dates = soup.select("div.col-4 > div.row > div.col-6 > p > span.Stat")
            dates = [element.text.strip() for element in parent_birth_dates]
            sire_birth_date = convert_birth_year(int(dates[0][-2:]))
            dam_birth_date = convert_birth_year(int(dates[1][-2:]))
                            
            # return following format:
            # rganimal rgpai  rgmae  siainterbull   paiinterbull  maeinterbull  sexo   datanas
            # origid   geno  
            animal_data = {
                "registration": registration,
                "sire_registration": sire_registration,
                "dam_registration": dam_registration,
                "sia_code": sia_code,
                "sire_sia_code": sire_sia_code,
                "dam_sia_code": dam_sia_code,  
                "sex": sia_code[6],
                "birth_year": birth_year,
                "country_id": sia_code[3:5],   
                "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
                "geno": '0'
            }
            
            sire_dict = {
                'sia_code': sire_sia_code,
                'birth_year': sire_birth_date
            }
            
            dam_dict = {
                'sia_code': dam_sia_code,
                'birth_year': dam_birth_date
            }
            
            return animal_data, sire_dict, dam_dict
                
        else:
            logging.warning(f"FAILED SCRAPING ANIMAL {sia_code}, CODE: {response.status_code}")
            animal_data = {
                "registration": registration,
                "sire_registration": '0',
                "dam_registration": '0',
                "sia_code": sia_code,
                "sire_sia_code": '0',
                "dam_sia_code": '0',  
                "sex": sia_code[6],
                "birth_year": '0',
                "country_id": sia_code[3:5],   
                "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
                "geno": '0'
            }
            
            return animal_data, None, None
    
    except httpx.RequestError as e:
        logging.error(f"Network error while scraping {sia_code}: {e}")
        animal_data = {
            "registration": registration,
            "sire_registration": '0',
            "dam_registration": '0',
            "sia_code": sia_code,
            "sire_sia_code": '0',
            "dam_sia_code": '0',  
            "sex": sia_code[6],
            "birth_year": '0',
            "country_id": sia_code[3:5],   
            "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
            "geno": '0'
        }
        
        return animal_data, None, None
    
    except Exception as e:
        logging.error(f"Parsing error for {sia_code} at URL {url}: {e}")
        animal_data = {
            "registration": registration,
            "sire_registration": '0',
            "dam_registration": '0',
            "sia_code": sia_code,
            "sire_sia_code": '0',
            "dam_sia_code": '0',  
            "sex": sia_code[6],
            "birth_year": '0',
            "country_id": sia_code[3:5],   
            "country_id_2": 'USA' if sia_code[3:6] == '840' else sia_code[3:6],           
            "geno": '0'
        }
        
        return animal_data, None, None
    
async def scrape_data_limited(session: httpx.AsyncClient, sia_code: str, special_case: bool):
    async with semaphore:
        return await scrape_data(session, sia_code, special_case)
