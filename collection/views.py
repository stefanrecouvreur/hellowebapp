from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect
from collection.forms import ProfileForm
from collection.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    # return view for index
    number = 6
    profiles = Profile.objects.all()
    return render(request, 'index.html', {
        'profiles': profiles,
    })


def profile_detail(request, slug):
    # grab the object
    profile = Profile.objects.get(slug=slug)
    # pass it to the template
    return render(request, 'profiles/profile_detail.html', {
        'profile': profile,
    })


@login_required
def edit_profile(request, slug):
    # grab the object
    profile = Profile.objects.get(slug=slug)
    # make sure the logged in user is the owner of the profile
    if profile.user != request.user:
            raise Http404
    # set the form we are using
    form_class = ProfileForm
    # if we're coming to this view from a submitted form
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=profile)
        if form.is_valid():
            # save the new data
            form.save()
            return redirect('profile_detail', slug=profile.slug)
    # otherwise just create the form
    else:
        form = form_class(instance=profile)

    # and render the template
    return render(request, 'profiles/edit_profile.html', {
        'profile': profile,
        'form': form,
    })

def create_profile(request):
    form_class(ProfileForm)
    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)
        if form.is_valid():
            # create an instance but do not save yet
            profile = form.save(commit=False)
            # set the additional details
            profile.user = request.user
            profile.slug = slugify(profile.name)
            # save the object
            profile.save()
            # redirect to our newly created profile
            return redirect('profile_detail', slug=profile.slug)
    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'profile/create_profile.html', {
        'form': form,
    })