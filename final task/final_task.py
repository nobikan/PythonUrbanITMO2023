# -*- coding: utf-8 -*-
"""Копия блокнота "PythonUrban_final_task.ipynb"

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_d9owt6p5Yna7TyZyZ37M9JdgVyea-vE

# Итоговый проект. Улицы. Объекты культурного наследия.
"""

# TODO собрать установку всех необходимых модулей в одном месте
!pip install geopandas mapclassify  # mapclassify для визуализации
!pip install osmnx  # устанавливаем модуль osmnx

# TODO собрать импорты всех модулей в одном месте
import osmnx as ox
import geopandas as gd

TILES = "CartoDB positron"  # Название подложки для карт

# TODO указать любой район Санкт-Петербург из OSM https://wiki.openstreetmap.org/wiki/RU:%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3/%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD%D1%8B
TERRITORY_NAME = 'Адмиралтейский'  # название территории для которой будут строиться слои

# TODO указать ссылку на файл из вашего github репозитория, которая начинается с https://raw.githubusercontent.com/
KGIOP_FILE_URL = "https://raw.githubusercontent.com/aeksei/PythonUrbanITMO2023/main/geojson_layers/bridges.geojson"  # ссылка на слой с объектами культурного наследия
STREETS_FILE_URL = "https://raw.githubusercontent.com/aeksei/PythonUrbanITMO2023/main/geojson_layers/streets.geojson"  # ссылка на слой с улицами

"""## Территория

### Загрузка территории из OSM (Extract)
"""

# TODO загрузить geodataframe с геометрией для территории TERRITORY_NAME
district = ox.geocode_to_gdf(f"{TERRITORY_NAME} район, Санкт-Петербург")

"""## Улицы

### Загрузка файла с улицами (Extract)
"""

# TODO отфильтровать улицы по маске геометрии территории полученной ранее
gdf = gd.read_file(STREETS_FILE_URL, mask=district)
#gdf.explore(tiles="CartoDB positron")

"""### Обработка данных с улицами (Transform)"""

# TODO сгруппировать и объединить геометрии с одинаковыми названиями
gdf = gdf.dissolve(by="name")

"""### Сохранение слоя с улицами (Load)"""

# TODO переименовать столбцы в русские названия, кроме столбца geometry
gdf.rename_axis('Названия улиц',inplace=True)
gdf
# TODO для того чтобы переименовать индекс, нужно обратиться и нему и вызвать от него метод rename (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.rename.html)

# TODO сохранить слой в географической проекции в формате GeoJSON
gdf.to_crs(4326).to_file('streets.geojson', driver='GeoJSON')

"""## Объекты культурного наследия

### Загрузка объектов культурного наследия (Extract)
"""

# TODO отфильтровать улицы по маске геометрии территории полученной ранее
kgiop = gd.read_file(KGIOP_FILE_URL, mask=district)

"""### Обработка объектов культурного наследия (Transform)"""

# TODO добавить два столбца lon и lat, в которых будут долгота и широта
kgiop["lon"] = kgiop.to_crs(3857).geometry.centroid.to_crs(4326).x
kgiop["lat"] = kgiop.to_crs(3857).geometry.centroid.to_crs(4326).y

"""### Сохранение слоя с объектами культурного наследия (Load)"""

# TODO переименовать столбцы в русские названия, кроме столбца geometry
kgiop.rename(columns={"Type":"Тип","Name": "Название","District": "Район","City function": "Городская функция","lon": "Долгота","lat": "Широта"}, inplace=True)
kgiop

# TODO сохранить слой в географической проекции в формате GeoJSON
kgiop.to_crs(4326).to_file('bridges.geojson', driver='GeoJSON')