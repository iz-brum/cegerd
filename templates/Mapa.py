import folium
import requests

# Criar um mapa centrado em uma coordenada específica (latitude, longitude)
mapa = folium.Map(location=[-13.3134, -55.9704], zoom_start=6)

# Coordenadas das cidades
cidades = {
    'Confresa': (-10.6413, -51.5698),
    'Sinop': (-11.8606, -55.5094),
    'Barra do Garças': (-15.8917, -52.2567),
    'Vila Bela da Santíssima Trindade': (-15.0067, -59.9500),
    'Pontes e Lacerda': (-15.2261, -59.3353),
    'Juína': (-11.3728, -58.7489),
    'Tangará da Serra': (-14.6229, -57.5000),
    'Diamantino': (-14.4032, -56.4379),
    'Cáceres': (-16.0769, -57.6819),
    'Jaciara': (-15.9548, -54.9682),
    'Colniza': (-9.4650, -60.0378),
    'Itiquira': (-17.2147, -54.1425),
    'Alta Floresta': (-9.8697, -56.0862), 
    'Sorriso': (-12.5422, -55.7219), 
    'Querência': (-12.6085, -52.1821),
    'Cuiabá': (-15.5989, -56.0949) 
}

API_KEY = "d2f43db503fef82f2052e803c234e2f2"
FIRMS_API_KEY = "0271d81cbe14958f860ce3be33c8a25e"

# Função para obter dados da FIRMS API (incêndios em tempo real)
def obter_focos_queimadas():
    url = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/0271d81cbe14958f860ce3be33c8a25e/VIIRS_SNPP_NRT/world/1"
    response = requests.get(url)
    linhas = response.text.split('\n')
    return [linha.split(',') for linha in linhas if linha]

# Obter focos de queimadas
focos_queimadas = obter_focos_queimadas()

# Adicionar marcadores para os focos de queimadas
for foco in focos_queimadas[1:]:
    latitude = float(foco[0])
    longitude = float(foco[1])
    folium.CircleMarker(location=[latitude, longitude], radius=5, color='red').add_to(mapa)

# Adicionar marcadores para as cidades e dados do clima e umidade
for cidade, coordenadas in cidades.items():
    lat, lon = coordenadas
    link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    umidade = requisicao_dic['main']['humidity']

    # Definir ícone e cor com base na temperatura
    if temperatura > 38:
        icone = folium.Icon(color='red')
    else:
        icone = folium.Icon(color='blue')
    
    # Adicionar pop-up com informações do clima e umidade
    pop_up = f"Cidade: {cidade}<br>Descrição: {descricao}<br>Temperatura: {temperatura:.2f}°C<br>Umidade: {umidade}%"
    folium.Marker(coordenadas, icon=icone, popup=folium.Popup(pop_up, parse_html=True)).add_to(mapa)

# Adicionar camada de mapa de satélite para Mato Grosso
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Esri', name='Esri Satellite', overlay=True).add_to(mapa)

# Salvar o mapa como um arquivo HTML
mapa.save('templates/mapa.html')

