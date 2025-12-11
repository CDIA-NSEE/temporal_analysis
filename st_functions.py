import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import pydeck as pdk
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, Point, MultiPoint

@st.cache_data(show_spinner="Carregando dados...")
def load_data(file_path: str, dtype: dict, date_cols: list) -> pd.DataFrame:

    df = pd.read_csv(file_path, dtype=dtype)

    for col_data in date_cols:
        df[col_data] = pd.to_datetime(df[col_data])
    
    return df


def geometrycollection_to_multipolygon(geometry_collection):
  if geometry_collection.geom_type == "GeometryCollection":
    polygons = []
    for geom in geometry_collection.geoms:
        if isinstance(geom, Polygon):
          # Adiciona o Polygon diretamente
          polygons.append(geom)
        elif isinstance(geom, MultiPolygon):
          # Divide MultiPolygon em polígonos individuais
          polygons.extend(geom.geoms)
        elif isinstance(geom, (LineString, MultiLineString, Point, MultiPoint)):
          polygons.append(geom.buffer(0.01))
    geometry_collection = MultiPolygon(polygons)
    # Retorna como MultiPolygon
  return geometry_collection

colors = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
    "#ffff33", "#a65628", "#f781bf", "#999999", "#66c2a5",
    "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f",
    "#e5c494", "#b3b3b3"
]

def choose_color(drs_id):
    return colors[(drs_id - 1) % len(colors)]

def style_drs(feature):
    return {
        "fillColor": choose_color(feature["properties"]["DRS"]),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6
    }

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


@st.cache_data(show_spinner="Carregando mapa...")
def load_map():
    drs_shapefile = gpd.read_file('datasets\sp_drs_group_interactive.kml').copy()
    drs_shapefile.drop(columns=['id','description', 'timestamp','begin','end','altitudeMode','tessellate','extrude','visibility','drawOrder','icon','CD_MUN','NM_MUN','SIGLA_UF','AREA_KM2'], inplace=True)
    NOME_DRS = ["Grande São Paulo", "Araçatuba", "Araraquara", "Baixada Santista", "Barretos", "Bauru", "Campinas", "Franca", "Marília", "Piracicaba", "Presidente Prudente", "Registro", "Ribeirão Preto", "São João da Boa Vista", "São José do Rio Preto", "Sorocaba", "Taubaté"]
    drs_shapefile['Nome'] = NOME_DRS
    #    drs_shapefile.rename(columns={'Name': 'DRS_completa'}, inplace = True)
    drs_shapefile.drop(columns=['Name'], inplace=True)

    NO_DRS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    drs_shapefile["DRS"] = NO_DRS
    drs_shapefile['geometry'] = drs_shapefile['geometry'].apply(lambda geom: geometrycollection_to_multipolygon(geom))
    drs_shapefile = gpd.GeoDataFrame(drs_shapefile, geometry='geometry')
    geojson = gpd.GeoDataFrame.to_json(drs_shapefile)

    m = folium.Map(location=[-22.9, -46.6], zoom_start=7)

    folium.GeoJson(
        geojson,
        name="DRS",
        style_function=style_drs,
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

def load_map_pydeck():

    # 1. LER E PREPARAR GEOMETRIAS -------------------------
    drs_shapefile = gpd.read_file('datasets/sp_drs_group_interactive.kml').copy()

    drs_shapefile.drop(columns=[
        'id','description', 'timestamp','begin','end','altitudeMode',
        'tessellate','extrude','visibility','drawOrder','icon',
        'CD_MUN','NM_MUN','SIGLA_UF','AREA_KM2'
    ], inplace=True)

    NOME_DRS = [
        "Grande São Paulo", "Araçatuba", "Araraquara", "Baixada Santista",
        "Barretos", "Bauru", "Campinas", "Franca", "Marília",
        "Piracicaba", "Presidente Prudente", "Registro", "Ribeirão Preto",
        "São João da Boa Vista", "São José do Rio Preto", "Sorocaba", "Taubaté"
    ]
    drs_shapefile['Nome'] = NOME_DRS
    drs_shapefile.drop(columns=['Name'], inplace=True)

    NO_DRS = list(range(1, 18))
    drs_shapefile["DRS"] = NO_DRS

    # Corrigir geometrias
    drs_shapefile['geometry'] = drs_shapefile['geometry'].apply(geometrycollection_to_multipolygon)

    # Converter para GeoJSON (dict, não string)
    geojson = json.loads(drs_shapefile.to_json())

    # 2. ADICIONAR CORES NO GEOJSON ------------------------
    for feature in geojson["features"]:
        drs_id = feature["properties"]["DRS"]
        r, g, b = hex_to_rgb(choose_color(drs_id))
        feature["properties"]["fill_color"] = [r, g, b, 170]  # 170 = opacidade

    # 3. CAMADA PYDECK -------------------------------------
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        stroked=True,
        filled=True,
        get_fill_color="properties.fill_color",
        get_line_color=[0, 0, 0],
        line_width_min_pixels=1,
        pickable=True,              # permite hover/click
        auto_highlight=True,        # highlight ao passar o mouse
    )

    # 4. VIEW ----------------------------------------------
    view_state = pdk.ViewState(
        latitude=-22.9,
        longitude=-46.6,
        zoom=7,
    )

    # 5. MAPA FINAL ----------------------------------------
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v9",
        tooltip={"text": "DRS: {Nome}"},
    )

    return deck