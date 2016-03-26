from django.shortcuts import render

# Create your views here.
def index(request):
    # return view for index
    number = 6
    thing = "Thing name"
    return render(request, 'index.html', {
        'number': number,
        'thing': thing,
    })
