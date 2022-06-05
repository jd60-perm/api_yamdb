from django.contrib import admin

from django.contrib import admin

from .models import (
    Comment, Review, Category, Genre, Title, User
)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        # 'author',
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


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)

