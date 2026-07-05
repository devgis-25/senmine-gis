from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance, Transform
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import numpy as np

from .models import (
    Region, SiteMinier, ExplorationMiniere, GisementMineral,
    CoursEau, AireProtegee, Localite, Route, LigneElectrique, Port
)
from .serializers import (
    RegionSerializer, SiteMiniérSerializer, ExplorationMiniereSerializer,
    GisementMineralSerializer, CoursEauSerializer, AireProtegeeSerializer,
    LocaliteSerializer, RouteSerializer, LigneElectriqueSerializer,
    PortSerializer, StatsSerializer, ConflitUsageSerializer, PredictionSerializer,ImpactEnvironnementalSerializer
)

from .impact import calculer_impact_site
 


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RegionSerializer

    def get_queryset(self):
        return Region.objects.all().annotate(geom_4326=Transform('geom', 4326))


class SiteMiniérViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteMiniérSerializer

    def get_queryset(self):
        return SiteMinier.objects.all().annotate(geom_4326=Transform('geom', 4326))


class ExplorationMiniereViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExplorationMiniereSerializer

    def get_queryset(self):
        return ExplorationMiniere.objects.all().annotate(geom_4326=Transform('geom', 4326))


class GisementMineralViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GisementMineralSerializer

    def get_queryset(self):
        return GisementMineral.objects.all().annotate(geom_4326=Transform('geom', 4326))


class CoursEauViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoursEauSerializer

    def get_queryset(self):
        return CoursEau.objects.all().annotate(geom_4326=Transform('geom', 4326))


class AireProtegeeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AireProtegeeSerializer

    def get_queryset(self):
        return AireProtegee.objects.all().annotate(geom_4326=Transform('geom', 4326))


class LocaliteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocaliteSerializer

    def get_queryset(self):
        return Localite.objects.all().annotate(geom_4326=Transform('geom', 4326))


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.all().annotate(geom_4326=Transform('geom', 4326))


class LigneElectriqueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LigneElectriqueSerializer

    def get_queryset(self):
        return LigneElectrique.objects.all().annotate(geom_4326=Transform('geom', 4326))


class PortViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortSerializer

    def get_queryset(self):
        return Port.objects.all().annotate(geom_4326=Transform('geom', 4326))


class StatsViewSet(viewsets.ViewSet):

    def list(self, request):
        nb_sites = SiteMinier.objects.count()
        nb_explorations = ExplorationMiniere.objects.count()
        nb_gisements = GisementMineral.objects.count()
        nb_aires = AireProtegee.objects.count()
        nb_localites = Localite.objects.count()

        # Nouveau code — vrais noms de substances
        substances_sites = list(
            SiteMinier.objects.exclude(substance=None)
            .exclude(substance='')
            .values_list('substance', flat=True)
            .distinct()
        )
        substances_exp = list(
            ExplorationMiniere.objects.exclude(substance=None)
            .exclude(substance='')
            .values_list('substance', flat=True)
            .distinct()
        )
        substances = list(set(substances_sites + substances_exp))

        # Régions minières actives
        regions = list(
            SiteMinier.objects.exclude(adm1=None)
            .exclude(adm1='')
            .values_list('adm1', flat=True)
            .distinct()
        )

        stats = {
            'nb_sites_miniers': nb_sites,
            'nb_explorations': nb_explorations,
            'nb_gisements': nb_gisements,
            'nb_aires_protegees': nb_aires,
            'nb_localites': nb_localites,
            'substances_principales': substances,  
            'regions_minieres': regions,
        }

        serializer = StatsSerializer(stats)
        return Response(serializer.data)


class ConflitUsageViewSet(viewsets.ViewSet):

    def list(self, request):
        sites = list(SiteMinier.objects.all())

        # Précharger TOUT en une seule requête chacun
        tous_cours_eau = list(CoursEau.objects.all())
        toutes_aires = list(AireProtegee.objects.all())

        resultats = []

        for site in sites:
            # Distance minimale cours d'eau
            dist_cours_eau = 999999
            for ce in tous_cours_eau:
                d = site.geom.distance(ce.geom)
                if d < dist_cours_eau:
                    dist_cours_eau = d

            # Distance minimale aire protégée
            dist_aire = 999999
            for aire in toutes_aires:
                d = site.geom.distance(aire.geom)
                if d < dist_aire:
                    dist_aire = d

            nb_localites = Localite.objects.filter(
                geom__distance_lte=(site.geom, 5000)
            ).count()

            score = 0
            if dist_cours_eau < 500: score += 30
            elif dist_cours_eau < 1000: score += 20
            elif dist_cours_eau < 5000: score += 10

            if dist_aire < 1000: score += 40
            elif dist_aire < 5000: score += 25
            elif dist_aire < 10000: score += 10

            if nb_localites >= 5: score += 30
            elif nb_localites >= 3: score += 20
            elif nb_localites >= 1: score += 10

            niveau = (
                'CRITIQUE' if score >= 70 else
                'ÉLEVÉ' if score >= 40 else
                'MODÉRÉ' if score >= 20 else
                'FAIBLE'
            )

            resultats.append({
                'site_id': site.fid,
                'site_nom': site.featurenam or 'Site inconnu',
                'site_type': site.featuretyp or 'Non défini',
                'substance': site.substance or 'Non défini',
                'region': site.adm1 or 'Non défini',
                'statut': site.locopstat or 'Non défini',
                'distance_cours_eau_m': round(dist_cours_eau, 2),
                'distance_aire_protegee_m': round(dist_aire, 2),
                'nb_localites_5km': nb_localites,
                'score_conflit': float(score),
                'niveau_risque': niveau,
            })

        resultats.sort(key=lambda x: x['score_conflit'], reverse=True)
        serializer = ConflitUsageSerializer(resultats, many=True)
        return Response(serializer.data)

class PredictionViewSet(viewsets.ViewSet):

    def list(self, request):
        regions = Region.objects.all()
        resultats = []

        sites_par_region = {}
        for site in SiteMinier.objects.all():
            region = site.adm1 or 'Inconnue'
            # Normaliser le nom pour matcher avec "Région de X"
            region_key = f"Région de {region}"
            if region_key not in sites_par_region:
                sites_par_region[region_key] = []
            sites_par_region[region_key].append(site)

        explorations_par_region = {}
        for exp in ExplorationMiniere.objects.all():
            region = exp.adm1 or 'Inconnue'
            region_key = f"Région de {region}"
            if region_key not in explorations_par_region:
                explorations_par_region[region_key] = []
            explorations_par_region[region_key].append(exp)


        gisements_par_region = {}
        for gis in GisementMineral.objects.all():
            region = gis.adm1 or 'Inconnue'
            region_key = f"Région de {region}"
            if region_key not in gisements_par_region:
                gisements_par_region[region_key] = []
            gisements_par_region[region_key].append(gis)

        for i, region in enumerate(regions):
            nom_region = region.name or f'Région {region.fid}'

            nb_sites = len(sites_par_region.get(nom_region, []))
            nb_exp = len(explorations_par_region.get(nom_region, []))
            nb_gis = len(gisements_par_region.get(nom_region, []))

            # Score de potentiel minier (0 à 100)
            # Basé sur : gisements connus + explorations actives + sites existants
            score = 0
            score += min(nb_gis * 20, 40)     # max 40 points pour les gisements
            score += min(nb_exp * 10, 30)     # max 30 points pour les explorations
            score += min(nb_sites * 5, 30)    # max 30 points pour les sites actifs

            # Substances probables basées sur les données réelles de la région
            substances = list(set(
                [s.substance for s in sites_par_region.get(nom_region, []) if s.substance and s.substance != '<null>'] +
                [e.substance for e in explorations_par_region.get(nom_region, []) if e.substance and e.substance != '<null>'] +
                [g.substance_principale for g in gisements_par_region.get(nom_region, []) if g.substance_principale and g.substance_principale != '<null>'] +
                [g.substance_secondaire for g in gisements_par_region.get(nom_region, []) if g.substance_secondaire and g.substance_secondaire != '<null>']
            ))

            # Recommandation
            if score >= 60:
                recommandation = 'Zone à fort potentiel — Prioriser les études de faisabilité'
            elif score >= 30:
                recommandation = 'Zone à potentiel modéré — Approfondir les explorations'
            elif score >= 10:
                recommandation = 'Zone à faible potentiel connu — Études géologiques recommandées'
            else:
                recommandation = 'Zone non explorée — Potentiel inconnu'

            resultats.append({
                'zone_id': region.fid,
                'region': nom_region,
                'score_potentiel': float(score),
                'substances_probables': substances,
                'facteurs': {
                    'nb_sites_actifs': nb_sites,
                    'nb_explorations': nb_exp,
                    'nb_gisements_connus': nb_gis,
                },
                'recommandation': recommandation,
            })

        # Trier par score décroissant
        resultats.sort(key=lambda x: x['score_potentiel'], reverse=True)

        serializer = PredictionSerializer(resultats, many=True)
        return Response(serializer.data)




class ImpactEnvironnementalViewSet(viewsets.ViewSet):

    def list(self, request):
        sites = SiteMinier.objects.all()
        resultats = []

        for site in sites:
            try:
                impact = calculer_impact_site(site)
                resultats.append(impact)
            except Exception as e:
                continue

        resultats.sort(key=lambda x: x['indice_risque'], reverse=True)
        serializer = ImpactEnvironnementalSerializer(resultats, many=True)
        return Response(serializer.data)    