from django.contrib import admin

from poetry_translation.models import Poem


class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'saved_by', 'updated_at', 'source_lang', 'target_lang', 'is_hidden']
    list_filter = ['is_hidden', 'created_at', 'source_lang', 'target_lang', 'saved_by']
    readonly_fields = ('created_at',)
    
    fieldsets = [
        (None, {"fields": ["is_hidden", "title", "author", "saved_by"]}),
        ("Text section", {"fields": ["original_text", "translation"]}),
        ("Translation settings", {"fields": ["source_lang", "target_lang", "language_engine"]}),
        ("Date information", {"fields": ["created_at", "updated_at"]}),
    ]


admin.site.register(Poem, PoemAdmin)
