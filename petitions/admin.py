from django.contrib import admin
from .models import Petition, PetitionVote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created')
    search_fields = ('title', 'created_by__username')

@admin.register(PetitionVote)
class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'petition', 'user', 'created')
    search_fields = ('petition__title', 'user__username')
