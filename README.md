# analise-ambiental-cascavel
🌍 Monitoramento Ambiental via Satélite: NDVI e NDWI (2005-2025)
Este repositório contém um script em Python desenvolvido para o Google Earth Engine. Ele foi criado originalmente para auxiliar em um TCC (Cascavel - CE), mas foi estruturado de forma totalmente adaptável para qualquer região do planeta.

🚀 O que este código faz?
O script processa imagens dos satélites Landsat 5 e 8 para gerar dois índices fundamentais:

NDVI (Vegetação): Identifica o vigor e a saúde da cobertura vegetal.

NDWI (Água): Identifica a presença de corpos hídricos e umidade no solo.

🛠️ "Plug and Play": Qualquer pessoa pode usar!
Este código foi pensado para ser acessível, mesmo para quem não domina programação. Para usar em outra cidade ou estado, basta alterar duas linhas:

Coordenadas: Insira a Latitude e Longitude do local desejado.

Área (Buffer): Defina o raio de alcance (ex: 20km para uma cidade, 50km para uma região).

📂 Como utilizar:
Copie o conteúdo de script_ambiental.py.

Cole em um novo notebook no Google Colab.

Autentique sua conta do Earth Engine (gratuito para fins acadêmicos).

O script gerará automaticamente arquivos GeoTIFF prontos para serem importados no QGIS, ArcGIS ou qualquer outro software de mapas.
