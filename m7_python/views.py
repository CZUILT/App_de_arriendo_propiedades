from django.shortcuts import render
from .services import get_all_inmuebles

# Create your views here.
def indexView(request):
    inmuebles = get_all_inmuebles()
    return render(request,'index.html',{'inmuebles':inmuebles} )