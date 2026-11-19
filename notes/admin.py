from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Note, Category, Tag

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "is_done", "created_at")
    list_filter = ("is_done",)
    search_fields = ("title", "text")

admin.site.register(Category)
admin.site.register(Tag)