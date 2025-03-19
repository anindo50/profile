from django.contrib import admin
from .models import NewsArticle

# Register your models here

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')  # Fields to display in the list view
    search_fields = ('title',) 

admin.site.register(NewsArticle, NewsArticleAdmin)