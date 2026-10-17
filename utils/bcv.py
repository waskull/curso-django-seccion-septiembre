import requests
from bs4 import BeautifulSoup

def obtener_dolar_bcv_manual():
    url = 'https://www.bcv.org.ve/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10) # verify=False por si hay problemas de SSL
        response.raise_for_status() # Lanza excepción si hay error HTTP
        
        # Parseamos el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        contenedor_dolar = soup.find('div', id='dolar')
        
        if contenedor_dolar:
            valor_texto = contenedor_dolar.find('strong').text.strip()
            
            valor_limpio = valor_texto.replace('.', '').replace(',', '.')
            
            return float(valor_limpio)
        else:
            return "No se pudo encontrar el contenedor del dólar en la página."

    except requests.exceptions.RequestException as e:
        return f"Error en la petición: {e}"
    except Exception as e:
        return f"Error al parsear los datos: {e}"

if __name__ == "__main__":
    precio = obtener_dolar_bcv_manual()
    if isinstance(precio, float):
        print(precio)
    else: print("error")