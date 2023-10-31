from django.contrib import admin

from .models import Recipe, UserProfile


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "ingredients", "cooking_time", "author")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the recipe
        if obj and request.user == obj.author:
            return True
        return super().has_delete_permission(request, obj)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(UserProfile)
