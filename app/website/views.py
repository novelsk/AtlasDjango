from django.contrib.auth.decorators import login_required
from atlas.models import AtlasUser
from .rabbit import main


@login_required
def rabbit_start(request):
    main()
