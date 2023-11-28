import folium
import requests
from googletrans import Translator

# Criar um mapa centrado em uma coordenada específica (latitude, longitude)
mapa = folium.Map(location=[-13.3134, -55.9704], zoom_start=6)

# Coordenadas das cidades
cidades = {
    'Água Boa': (-14.0504, -52.1606),
    'Arenápolis': (-14.4473, -56.8531),
    'Barão de Melgaço': (-16.2060, -55.9671),
    'Barra do Garças': (-15.8833, -52.2569),
    'Cáceres': (-16.0735, -57.6819),
    'Campo Novo do Parecis': (-13.6681, -57.8903),
    'Chapada dos Guimarães': (-15.4649, -55.7497),
    'Comodoro': (-13.6618, -59.7847),
    'Confresa': (-10.6346, -51.5696),
    'Cuiabá': (-15.5989, -56.0949),
    'Feliz Natal': (-12.3840, -54.9223),
    'Nova Canaã do Norte': (-10.5580, -55.7276),
    'Nova Olímpia': (-14.7958, -57.2880),
    'Paranatinga': (-14.4265, -54.0510),
    'Peixoto de Azevedo': (-10.2269, -54.9794),
    'Pontes de Lacerda': (-15.2290, -59.3381),
    'Poxoréu': (-15.8295, -54.4011),
    'Rondonópolis': (-16.4676, -54.6372),
    'Santa Terezinha': (-10.4704, -50.5141),
    'Santo Antônio do Leverger': (-15.8653, -56.0789),
    'São José do Rio Claro': (-13.4606, -56.7216),
    'Vila Rica': (-10.0192, -51.1189),
    'Tangará da Serra': (-14.6229, -57.5000),
    'Sorriso': (-12.5422, -55.7219),
    'Guarantã do Norte': (-9.97063, -54.9049),
    'Alto Araguaia': (-17.3164, -53.2199),
    'Apiacás': (-9.54007, -57.4596),
    'Sapezal': (-13.5403, -58.2441),
    'Campo Verde': (-15.5408, -55.1606),
    'Juara': (-11.2634, -57.5242),
    'Querência': (-12.6102, -52.1826),
    'Sinop': (-11.8668, -55.5081),
    'Cotriguaçu': (-9.85753, -58.4198),
    'Juína': (-11.3728, -58.7489),
    'São Félix do Araguaia': (-11.6144, -50.6704),
    'Vila Bela da Santíssima Trindade': (-15.0067, -59.9500),
    'Primavera do Leste': (-15.5950, -54.2990),
    'Alta Floresta': (-9.8697, -56.0862),
    'Carlinda': (-9.94915, -55.8415),
    'Brasnorte': (-12.1472, -57.9833),
    'Nova Maringá': (-13.0136, -57.0907),
    'Nova Ubiratã': (-12.9830, -55.2567),
    'Gaúcha do Norte': (-13.2427, -53.0809),
    'Santo Antônio do Leste': (-14.8058, -53.6155),
    'Guiratinga': (-16.3466, -53.7576),
    'Itiquira': (-17.2147, -54.1425),
    'Alto Taquari': (-17.8350, -53.2792),
    'Porto Estrela': (-15.3230, -57.2204),
    'Salto do Céu': (-15.1307, -58.1323),
    'São José do Xingu': (-10.7983, -52.7486),
    'Serra Nova Dourada': (-12.0899, -51.7659),
    'Rosário Oeste': (-14.8406, -56.4307),
    'Canarana': (-13.5512, -52.2705),
    'Nova Xavantina': (-14.6774, -52.3506),
    'Serra Nova Dourada': (-12.0899, -51.7659),
    'Nova Ubiratã': (-12.9830, -55.2567),
    'Diamantino': (-14.4032, -56.4379)
}

API_KEY = "d2f43db503fef82f2052e803c234e2f2"
FIRMS_API_KEY = "5184f331c2b6a817cd5a21d0c6880681"

# Função para obter dados da FIRMS API (incêndios em tempo real)
def obter_focos_queimadas():
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{FIRMS_API_KEY}/VIIRS_SNPP_NRT/world/1"
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
    link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt"  # Adicionei o parâmetro lang=pt
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    umidade = requisicao_dic['main']['humidity']
    chuva = 'chuva' in descricao.lower()  # Verifica se a descrição contém a palavra "rain"
   
    # Definir ícone e cor com base na temperatura e chuva
    if temperatura > 38:
        icone = folium.Icon(color='red')
    elif chuva:
        icone = folium.Icon(color='yellow')
    else:
        icone = folium.Icon(color='blue')
    
    # Adicionar pop-up com informações do clima e umidade
    pop_up = f"Cidade: {cidade}<br>Descrição: {descricao}<br>Temperatura: {temperatura:.2f}°C<br>Umidade: {umidade}%"
    folium.Marker(coordenadas, icon=icone, popup=folium.Popup(pop_up, parse_html=True)).add_to(mapa)


# Adicionar camada de mapa do OpenStreetMap
folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', attr='OpenStreetMap', name='OpenStreetMap').add_to(mapa)

# Salvar o mapa como um arquivo HTML
mapa.save('templates/mapa.html')

