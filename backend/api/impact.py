import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping, Point as ShapelyPoint
from shapely.ops import transform as shapely_transform
import numpy as np
import pyproj
from django.contrib.gis.db.models.functions import Distance
from .models import CoursEau, AireProtegee, Localite

WORLDPOP_PATH = r'C:/Users/user/Desktop/projets/projet_web_gis/senmine/data/raw/sen_pop_2020_CN_100m_R2025A_v1.tif'

# Transformer 32628 → 4326 réutilisable
_transformer = pyproj.Transformer.from_crs('EPSG:32628', 'EPSG:4326', always_xy=True)

def _to_4326(geom_shapely):
    return shapely_transform(_transformer.transform, geom_shapely)


def calculer_impact_site(site):
    from shapely.geometry import Point as ShapelyPoint

    point = ShapelyPoint(site.geom.x, site.geom.y)
    point_4326 = _to_4326(point)
    lon, lat = point_4326.x, point_4326.y

    resultats = {}

    for rayon_km in [5, 10, 20]:
        rayon_m = rayon_km * 1000
        tampon_32628 = point.buffer(rayon_m)
        tampon_4326 = _to_4326(tampon_32628)

        population = 0
        try:
            with rasterio.open(WORLDPOP_PATH) as src:
                # Vérifier que le tampon chevauche le raster
                from shapely.geometry import box
                raster_bounds = box(*src.bounds)
                if tampon_4326.intersects(raster_bounds):
                    geom_mask = [mapping(tampon_4326)]
                    out_image, _ = mask(src, geom_mask, crop=True, nodata=-9999)
                    data = out_image[0]
                    valid = data[(data > 0) & (data < 1e6)]
                    population = int(np.nansum(valid))
        except Exception as e:
            population = 0

        nb_localites = Localite.objects.filter(
            geom__distance_lte=(site.geom, rayon_m)
        ).count()

        resultats[f'rayon_{rayon_km}km'] = {
            'population': population,
            'nb_localites': nb_localites,
        }

    # Distances
    cours_proche = CoursEau.objects.annotate(
        dist=Distance('geom', site.geom)
    ).order_by('dist').first()
    dist_eau = cours_proche.dist.m if cours_proche else 999999

    aire_proche = AireProtegee.objects.annotate(
        dist=Distance('geom', site.geom)
    ).order_by('dist').first()
    dist_aire = aire_proche.dist.m if aire_proche else 999999

    dist_eau_km = dist_eau / 1000
    dist_aire_km = dist_aire / 1000
    pop_5km = resultats['rayon_5km']['population']

    risque = 0
    if dist_eau_km < 0.5: risque += 30
    elif dist_eau_km < 1: risque += 20
    elif dist_eau_km < 5: risque += 10

    if dist_aire_km < 1: risque += 40
    elif dist_aire_km < 5: risque += 25
    elif dist_aire_km < 10: risque += 10

    if pop_5km > 50000: risque += 30
    elif pop_5km > 10000: risque += 20
    elif pop_5km > 1000: risque += 10

    return {
        'site_id': site.fid,
        'site_nom': site.featurenam or 'Site inconnu',
        'substance': site.substance or 'N/A',
        'region': site.adm1 or 'N/A',
        'statut': site.locopstat or 'N/A',
        'lat': round(lat, 6),
        'lon': round(lon, 6),
        'distance_cours_eau_km': round(dist_eau_km, 2),
        'distance_aire_protegee_km': round(dist_aire_km, 2),
        'population_5km': resultats['rayon_5km']['population'],
        'population_10km': resultats['rayon_10km']['population'],
        'population_20km': resultats['rayon_20km']['population'],
        'localites_5km': resultats['rayon_5km']['nb_localites'],
        'localites_10km': resultats['rayon_10km']['nb_localites'],
        'localites_20km': resultats['rayon_20km']['nb_localites'],
        'indice_risque': risque,
        'niveau_risque': (
            'CRITIQUE' if risque >= 70 else
            'ÉLEVÉ' if risque >= 40 else
            'MODÉRÉ' if risque >= 20 else
            'FAIBLE'
        )
    }