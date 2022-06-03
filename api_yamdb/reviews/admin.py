from django.contrib import admin

from django.contrib import admin

from .models import (
    Comment, Review, Category, Genre, Title
)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        # 'author',
        'review',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        # 'author',
        'score',
        'title',
    )
    list_editable = ('title',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
