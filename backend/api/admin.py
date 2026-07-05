from django.contrib import admin
from .models import (
    Region, SiteMinier, ExplorationMiniere, GisementMineral,
    CoursEau, AireProtegee, Localite, Route, LigneElectrique, Port
)


@admin.register(SiteMinier)
class SiteMiniérAdmin(admin.ModelAdmin):
    list_display = ['fid', 'featurenam', 'featuretyp', 'substance', 'adm1', 'locopstat']
    search_fields = ['featurenam', 'substance', 'adm1', 'operatenam']
    list_filter = ['locopstat', 'adm1', 'featuretyp']
    exclude = ['geom']


@admin.register(ExplorationMiniere)
class ExplorationMiniereAdmin(admin.ModelAdmin):
    list_display = ['fid', 'featurenam', 'substance', 'adm1', 'locopstat']
    search_fields = ['featurenam', 'substance', 'adm1']
    list_filter = ['locopstat', 'adm1']
    exclude = ['geom']


@admin.register(GisementMineral)
class GisementMineralAdmin(admin.ModelAdmin):
    list_display = ['fid', 'featurenam', 'substance_principale', 'adm1']
    search_fields = ['featurenam', 'substance_principale', 'adm1']
    list_filter = ['adm1']
    exclude = ['geom']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name', 'admin_level']
    search_fields = ['name']
    exclude = ['geom']


@admin.register(AireProtegee)
class AireProtegeeAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name']
    search_fields = ['name']
    exclude = ['geom']


@admin.register(Localite)
class LocaliteAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name', 'place']
    search_fields = ['name']
    exclude = ['geom']


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ['fid', 'featurenam']
    search_fields = ['featurenam']
    exclude = ['geom']