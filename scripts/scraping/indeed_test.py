#ESTE TEST AUNQUE FUE CREADO PARA INDEED FUNCIONA PARA CUALQUIER PAGINA

import requests

url = "https://pe.computrabajo.com/trabajo-de-software"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)

print("Código:", r.status_code)
print("Contiene 'mosaic-provider-jobcards':", "mosaic-provider-jobcards" in r.text)
print("Contiene 'Ejecutivo':", "Ejecutivo" in r.text)
print("Longitud HTML:", len(r.text))

with open("indeed.html", "w", encoding="utf-8") as f:
    f.write(r.text)