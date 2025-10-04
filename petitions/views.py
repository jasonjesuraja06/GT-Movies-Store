from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from .models import Petition, PetitionVote

def index(request):
    # Show all petitions with their YES counts; show create form if logged in
    template_data = {
        'title': 'Petitions',
        'petitions': Petition.objects.select_related('created_by').prefetch_related('votes').order_by('-created')
    }
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    if request.method != 'POST':
        return redirect('petitions.index')

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()

    if not title:
        return redirect('petitions.index')  # keep it simple for the practical

    Petition.objects.create(
        title=title,
        description=description,
        created_by=request.user
    )
    return redirect('petitions.index')

@login_required
def vote_yes(request, id):
    if request.method != 'POST':
        return redirect('petitions.index')

    petition = get_object_or_404(Petition, id=id)
    try:
        PetitionVote.objects.create(petition=petition, user=request.user)
    except IntegrityError:
        # user already voted yes on this petition -> ignore duplicate
        pass
    return redirect('petitions.index')
