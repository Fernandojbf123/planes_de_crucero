def get_lon_lat_max_and_min(navegacion):
    latitudes = navegacion["latitudes_plan"]
    longitudes = navegacion["longitudes_plan"]
    
    lat_min = round(min(latitudes)-0.1,2)
    lat_max = round(max(latitudes)+1,2)
    lon_min = round(min(longitudes)-0.7,2)
    lon_max = round(max(longitudes)+0.7,2)
    
    return lon_min, lon_max, lat_min, lat_max