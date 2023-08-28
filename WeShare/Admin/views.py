from django.shortcuts import HttpResponse,redirect,render

# Create your views here.
def helloadmin(request):
    return render(request,"Admin/admin.html",{})
