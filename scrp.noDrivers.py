import os, requests,time,json,urllib.parse
from dotenv import load_dotenv as load
from bs4 import BeautifulSoup, Tag


load()

crestUrl=os.getenv('Url_crest')
uAgent=str(os.getenv('Agent'))

all_what_i_have=[]
def is_valid_product(product_data):
    key_attributes = ["brand", "model", "regular_price"]
    return any(product_data.get(attr) != "Nope" for attr in key_attributes)

def extract_product_data(article:Tag):
    product_data = {}
    
    product_data["id"] = article.get("id", "Nope")
    
    try:
        product_data["link"] = urllib.parse.urljoin(crestUrl, article.select_one("a.no_decoration")["href"])
    except:
        product_data["link"] = "Nope"
    
    # Ціни
    try:
        product_data["financed_price"] = article.select_one("div.vehiculo-price.financiado").text.strip()
    except:
        product_data["financed_price"] = "Nope"
    try:
        product_data["regular_price"] = article.select_one("div.vehiculo-price.coche.oferta:not(.financiado)").text.strip()
    except:
        product_data["regular_price"] = "Nope"
    try:
        product_data["old_price"] = article.select_one("div.vehiculo-price.old_precio").text.strip()
    except:
        product_data["old_price"] = "Nope"
    try:
        product_data["monthly_price"] = article.select_one("div.vehiculo-price.right").text.strip()
    except:
        product_data["monthly_price"] = "Nope"
    
    # URL зображень
    try:
        img_block = article.select_one("div.vehiculo_shop_imagen img:not(.etiqueta_eco)")
        product_data["image_url"] = img_block["src"] if img_block else "Nope"
    except:
        product_data["image_url"] = "Nope"
    
    
    # Дані автомобіля
    try:
        product_data["brand"] = article.select_one("h4 span.marca").text.strip()
    except:
        product_data["brand"] = "Nope"
    try:
        product_data["model"] = article.select_one("h4 span.modelo").text.strip()
    except:
        product_data["model"] = "Nope"
    try:
        product_data["trim"] = article.select_one("h4 span.acabado").text.strip()
    except:
        product_data["trim"] = "Nope"
    try:
        product_data["year"] = article.select_one("h4 span.vehiculo_year").text.strip()
    except:
        product_data["year"] = "Nope"
    try:
        mileage = article.select_one("div.veh_div_lista:nth-of-type(1)")
        product_data["mileage"] = mileage.text.strip() if mileage else "Nope"
    except:
        product_data["mileage"] = "Nope"
    try:
        fuel = article.select_one("div.veh_div_lista:nth-of-type(2)")
        product_data["fuel"] = fuel.text.strip() if fuel else "Nope"
    except:
        product_data["fuel"] = "Nope"
    try:
        transmission = article.select_one("div.veh_div_lista:nth-of-type(3)")
        product_data["transmission"] = transmission.text.strip() if transmission else "Nope"
    except:
        product_data["transmission"] = "Nope"
    try:
        power = article.select_one("div.veh_div_lista:nth-of-type(4)")
        product_data["power"] = power.text.strip() if power else "Nope"
    except:
        product_data["power"] = "Nope"
    
    return product_data

def scrape_it(id:int):
    headers = {'User-Agent': uAgent}
    response = requests.get(crestUrl+str(id), headers=headers)

# ##    *тут перевірка чи вийде під'єднатись*
#     if response.status_code == 200:print("Yeeyy")
#     else:raise ValueError("Nope(")

    if response.status_code==200:
        soup = BeautifulSoup(response.text, "html.parser")
        product_cards = soup.select("article.vehiculo_shop")
        
        for card in product_cards:
            product_data = extract_product_data(card)
            if is_valid_product(product_data):
                all_what_i_have.append(product_data)
            else:
                print(f"Invalid: {product_data['id']}")
    else:
        print(f"Err: {response.status_code}")

scrape_it(1)
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(all_what_i_have, f, ensure_ascii=False, indent=4)


all_what_i_get=[]
def scrapeFromBack(page:int):
    headers = {
        "User-Agent": uAgent,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"{crestUrl}{page}",
    }
    
    data = {
        "datos_consulta": "order=mas_recientes&marca=&precio=0&km=0&iva=0&anio=0&plazas=0&desde_km=0&hasta_km=0&desde_cc=0&hasta_cc=0",
        "datos_segmentos": "",
        "datos_combustible": "",
        "datos_carnet": "",
        "datos_cambio": "",
        "datos_etiqueta": "",
        "datos_tipos_de_moto": "",
        "pagina": str(page),
        "ciudad": "",
        "marca": "",
        "modelo": ""
    }

    try:
        response=requests.post(os.getenv('API_crest'),headers=headers,data=data)
        if response.status_code!=200:print(f"Error:{response.status_code}");return False
        try:
            data_json_from =response.json()
            if data_json_from.get("result") != 1 or not data_json_from.get("html"):print(f"ParsingError:{Nooooo}");return False
            
            soupe=BeautifulSoup(data_json_from['html'],'lxml')
            cards=soupe.select("article.vehiculo_shop")
            if not cards:print("You Don't Have the Cards");return False
            
            for card in cards:
                product_data = extract_product_data(card)
                if is_valid_product(product_data) and product_data["id"] not in [p["id"] for p in all_what_i_get]:
                    all_what_i_get.append(product_data)
                else:
                    print(f"Invalid: {product_data['id']}")
            
            return True
        except ValueError as Nooooo:print(f"ParsingError:{Nooooo}");return False
        
    except Exception as Nooooo:print(f"Error:{Nooooo}");return False
for Iter in range(0,105):scrapeFromBack(Iter)
with open("cards.json", "w", encoding="utf-8") as f:
    json.dump(all_what_i_get, f, ensure_ascii=False, indent=4)

