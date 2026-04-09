import ee
import geemap

# 1. INICIALIZAÇÃO
try:
    ee.Initialize(project='tccdomatheus')
except:
    ee.Authenticate()
    ee.Initialize(project='tccdomatheus')

# 2. ÁREA DE ESTUDO (Cascavel - CE)
ponto = ee.Geometry.Point([-38.2435, -4.1332])
area_estudo = ponto.buffer(20000).bounds()

# 3. FUNÇÃO PARA PROCESSAR OS DADOS
def gerar_mapa_ano(ano, satelite):
    colecao = ee.ImageCollection(satelite) \
        .filterBounds(area_estudo) \
        .filterDate(f'{ano-1}-01-01', f'{ano+1}-12-31') \
        .filter(ee.Filter.lt('CLOUD_COVER', 30))
    
    imagem = colecao.median().clip(area_estudo)
    
    # Cálculo para Landsat 8 (2015 e 2025) e Landsat 5 (2005)
    if 'LC08' in satelite:
        ndvi = imagem.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    else:
        ndvi = imagem.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
    return ndvi

# 4. PROCESSANDO OS TRÊS ANOS
ndvi_2005 = gerar_mapa_ano(2005, "LANDSAT/LT05/C02/T1_L2")
ndvi_2015 = gerar_mapa_ano(2015, "LANDSAT/LC08/C02/T1_L2")
ndvi_2025 = gerar_mapa_ano(2025, "LANDSAT/LC08/C02/T1_L2")

# 5. CONFIGURAÇÃO DO MAPA
Map = geemap.Map()
Map.centerObject(ponto, 11)
Map.add_basemap('SATELLITE')

# Cores: Vermelho (seco) -> Amarelo -> Verde (saudável)
vis_params = {'min': 0, 'max': 0.6, 'palette': ['red', 'yellow', 'green']}

# 6. ADICIONANDO AS CAMADAS AO MAPA
# Elas vão aparecer no ícone de "Layers" (folhinhas) no canto do mapa
Map.addLayer(ndvi_2005, vis_params, 'NDVI 2005 (Landsat 5)')
Map.addLayer(ndvi_2015, vis_params, 'NDVI 2015 (Landsat 8)')
Map.addLayer(ndvi_2025, vis_params, 'NDVI 2025 (Landsat 8)')

# Adiciona uma legenda para o Matheus saber o que as cores significam
Map.add_colorbar(vis_params, label="Índice de Vegetação (NDVI)")

Map # Exibe o mapa

#Essa é a segunda parte, indico fazer separado no COLAB
# ---------------------------------------------------------
# CÉLULA DE DOWNLOAD: EXPORTAR NDVI E NDWI (2005, 2015, 2025)
# ---------------------------------------------------------

print("Iniciando a criação dos arquivos GeoTIFF... Aguarde.")

# Lista para facilitar o loop
anos_estudo = [2005, 2015, 2025]
satelites_estudo = ["LANDSAT/LT05/C02/T1_L2", "LANDSAT/LC08/C02/T1_L2", "LANDSAT/LC08/C02/T1_L2"]

for ano, sat in zip(anos_estudo, satelites_estudo):
    # Reutiliza a lógica para processar os dados brutos
    colecao = ee.ImageCollection(sat) \
        .filterBounds(area_estudo) \
        .filterDate(f'{ano-1}-01-01', f'{ano+1}-12-31') \
        .sort('CLOUD_COVER')
    
    imagem = colecao.median().clip(area_estudo)
    
    # Cálculos de NDVI (Vegetação) e NDWI (Água)
    if 'LC08' in sat:
        ndvi = imagem.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
        ndwi = imagem.normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI')
    else:
        ndvi = imagem.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
        ndwi = imagem.normalizedDifference(['SR_B2', 'SR_B4']).rename('NDWI')
    
    # Exportação para a pasta do Colab
    geemap.ee_export_image(ndvi, filename=f'NDVI_Cascavel_{ano}.tif', scale=30, region=area_estudo)
    geemap.ee_export_image(ndwi, filename=f'NDWI_Cascavel_{ano}.tif', scale=30, region=area_estudo)
    
    print(f"✅ Arquivos de {ano} prontos!")

print("\n--- TUDO CONCLUÍDO ---")
print("Clique no ícone da PASTA à esquerda e faça o download dos 6 arquivos .tif")
