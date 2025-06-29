from django.contrib import admin
from .models import Tag

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'color', 'created_at']
    list_filter = ['type']
    search_fields = ['name']
    ordering = ['type', 'name']
    fieldsets = (
        (None, {'fields': ('name', 'type', 'color')}),
        ('Metadaten', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
