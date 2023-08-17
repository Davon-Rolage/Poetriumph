from django.contrib import admin

from poetry_translation.models import Poem


class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'saved_by', 'updated_at', 'source_lang', 'target_lang']
    list_filter = ['created_at', 'source_lang', 'target_lang', 'saved_by']
    readonly_fields = ('created_at',)
    
    fieldsets = [
        (None, {"fields": ["title", "author", "saved_by"]}),
        ("Text section", {"fields": ["original_text", "translation"]}),
        ("Translation settings", {"fields": ["source_lang", "target_lang", "language_engine"]}),
        ("Date information", {"fields": ["created_at", "updated_at"]}),
    ]


admin.site.register(Poem, PoemAdmin)
