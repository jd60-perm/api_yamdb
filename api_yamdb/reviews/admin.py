from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'review',
    )
    search_fields = ('review', 'author',)
    list_filter = ('review', 'author',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'score',
        'title',
    )
    #list_editable = ('title',)
    search_fields = ('title',)
    list_filter = ('title', 'author')
    #empty_value_display = '-empty-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'bio', 'role')
    search_fields = ('first_name', 'last_name')
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description',)
    search_fields = ('name','description',)
    list_filter = ('name', 'description',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
admin.site.register(Title, TitleAdmin)
