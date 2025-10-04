from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    # The movie the user wants the admin to include
    title = models.CharField(max_length=120)
    # Optional extra context for the request
    description = models.TextField(blank=True)
    # Who posted the petition
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PetitionVote(models.Model):
    petition = models.ForeignKey(
        Petition,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One YES vote per user per petition
        unique_together = ('petition', 'user')

    def __str__(self):
        return f'{self.user.username} → {self.petition.title}'
