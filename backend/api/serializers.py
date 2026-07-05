from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework import serializers
from .models import (
    Region, SiteMinier, ExplorationMiniere, GisementMineral,
    CoursEau, AireProtegee, Localite, Route, LigneElectrique, Port
)


class RegionSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = Region
        geo_field = 'geom_4326'
        fields = ['fid', 'osm_id', 'name', 'admin_level', 'geom_4326']


class SiteMiniérSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = SiteMinier
        geo_field = 'geom_4326'
        fields = [
            'fid', 'featurenam', 'featuretyp', 'secteur',
            'categorie', 'substance', 'country', 'adm1',
            'locopstat', 'operatenam', 'ownername1', 'geom_4326'
        ]


class ExplorationMiniereSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = ExplorationMiniere
        geo_field = 'geom_4326'
        fields = [
            'fid', 'featurenam', 'substance',
            'country', 'adm1', 'locopstat',
            'ownername', 'geom_4326'
        ]


class GisementMineralSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = GisementMineral
        geo_field = 'geom_4326'
        fields = [
            'fid', 'featurenam', 'substance_principale',
            'substance_secondaire', 'substance_tertiaire',
            'country', 'adm1', 'geom_4326'
        ]


class CoursEauSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = CoursEau
        geo_field = 'geom_4326'
        fields = ['fid', 'name', 'waterway', 'geom_4326']


class AireProtegeeSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = AireProtegee
        geo_field = 'geom_4326'
        fields = ['fid', 'name', 'boundary', 'geom_4326']


class LocaliteSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = Localite
        geo_field = 'geom_4326'
        fields = ['fid', 'name', 'place', 'geom_4326']


class RouteSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()
    class Meta:
        model = Route
        geo_field = 'geom_4326'
        fields = ['fid', 'featurenam', 'geom_4326']

class LigneElectriqueSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()
    class Meta:
        model = LigneElectrique
        geo_field = 'geom_4326'
        fields = ['fid', 'voltage', 'voltage_classification', 'geom_4326']

class PortSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()
    class Meta:
        model = Port
        geo_field = 'geom_4326'
        fields = ['fid', 'featurenam', 'geom_4326']


class StatsSerializer(serializers.Serializer):
    nb_sites_miniers = serializers.IntegerField()
    nb_explorations = serializers.IntegerField()
    nb_gisements = serializers.IntegerField()
    nb_aires_protegees = serializers.IntegerField()
    nb_localites = serializers.IntegerField()
    substances_principales = serializers.ListField()
    regions_minieres = serializers.ListField()


class ConflitUsageSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
    site_nom = serializers.CharField()
    site_type = serializers.CharField()
    substance = serializers.CharField()
    region = serializers.CharField()
    statut = serializers.CharField()
    distance_cours_eau_m = serializers.FloatField()
    distance_aire_protegee_m = serializers.FloatField()
    nb_localites_5km = serializers.IntegerField()
    score_conflit = serializers.FloatField()
    niveau_risque = serializers.CharField()


class PredictionSerializer(serializers.Serializer):
    zone_id = serializers.IntegerField()
    region = serializers.CharField()
    score_potentiel = serializers.FloatField()
    substances_probables = serializers.ListField()
    facteurs = serializers.DictField()
    recommandation = serializers.CharField()
    
    

class ImpactEnvironnementalSerializer(serializers.Serializer):
    site_id = serializers.IntegerField()
    site_nom = serializers.CharField()
    substance = serializers.CharField()
    region = serializers.CharField()
    statut = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    distance_cours_eau_km = serializers.FloatField()
    distance_aire_protegee_km = serializers.FloatField()
    population_5km = serializers.IntegerField()
    population_10km = serializers.IntegerField()
    population_20km = serializers.IntegerField()
    localites_5km = serializers.IntegerField()
    localites_10km = serializers.IntegerField()
    localites_20km = serializers.IntegerField()
    indice_risque = serializers.FloatField()
    niveau_risque = serializers.CharField() 

    