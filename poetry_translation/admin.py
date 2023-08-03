from django.contrib import admin
from poetry_translation.models import Poem


class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'source_lang', 'target_lang']
    list_filter = ['created_at', 'source_lang', 'target_lang']
    readonly_fields = ('created_at',)
    
    fieldsets = [
        (None, {"fields": ["title", "user_text", "text"]}),
        ("Translation settings", {"fields": ["source_lang", "target_lang", "language_engine"]}),
        ("Date information", {"fields": ["created_at", "updated_at"]}),
    ]


admin.site.register(Poem, PoemAdmin)
