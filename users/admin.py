from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from users.forms import UserAdminChangeForm, UserAdminCreationForm
from users.models import User, MovieRank, MovieSeen


class MovieSeenAdmin(admin.TabularInline):
    model = User.movies_seen.through


class MovieFavoritesAdmin(admin.TabularInline):
    model = User.favorites_movies.through


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info',
         {'fields': ('name', 'lastname')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'lastname', 'email', 'password1', 'password2',)
        }
         ),
    )
    inlines = (MovieSeenAdmin, MovieFavoritesAdmin)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(MovieRank)
admin.site.register(MovieSeen)
