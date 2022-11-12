from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    fields = ('name', 'slug')
    ordering = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    fields = ('name', 'slug')
    ordering = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    fields = ('name', 'year', 'description', 'genre', 'category')
    ordering = ('name', 'year')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('name', 'year')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'score', 'pub_date', 'title')
    fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    ordering = ('id', 'author')
    search_fields = ('id', 'author')
    list_filter = ('id', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date',)
    fields = ('id', 'author', 'pub_date', 'review')
    ordering = ('id', 'author')
    search_fields = ('id', 'author')
    list_filter = ('id', 'author')
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
