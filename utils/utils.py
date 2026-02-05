import datetime
from urllib.parse import urlparse, parse_qs

def sia_code_to_url(sia_code: str) -> str:
    base_url = "https://lactanetgen.ca/query/summary.php?breed=HO"
    
    animal_country_code = sia_code[3:6]
    animal_sex = sia_code[6]
    animal_regnum = int(sia_code[7:])
    
    url = (
        base_url +
        "&country=" + animal_country_code +
        "&sex=" + animal_sex +
        "&regnum=" + str(animal_regnum)
    )
    
    return url

def sia_code_to_registration(sia_code: str) -> str:
    registration = sia_code[3:5] + sia_code[7:].lstrip("0")

    return registration 
    
def url_to_animal_data(url) -> str:
    # 1. Analisa a URL para separar seus componentes
    parsed_url = urlparse(url)
    # print(f"Extracted query string: {parsed_url.query}")

    # 2. Transforma a query string em um dicionário
    # Os valores do dicionário são listas, pois um parâmetro pode aparecer várias vezes
    params = parse_qs(parsed_url.query)
    # print(f"Params dictionary: {params}")

    # 3. Extrai o primeiro valor de cada parâmetro desejado
    # Usamos [0] para pegar o primeiro (e único) item da lista
    country = params['country'][0]
    sex = params['sex'][0]
    registration_number = params['regnum'][0]

    # 4. Concatena os valores para formar a string final
    sia_code = 'HOL' + country + sex + registration_number.zfill(12)
    registration = country[:2] + registration_number

    # print(f"\nResultado Final: {resultado_final}")
    return sia_code, registration

def convert_birth_year(year):
    try:
        year = int(year)
        ano_atual_yy = datetime.now().year % 100
        
        if year <= ano_atual_yy:
            return 2000 + year
        else:
            return 1900 + year
            
    except (ValueError, TypeError, IndexError):
        # debugando
        print(f"{year} {len(year)}")
        return 1911
