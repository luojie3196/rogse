from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from blog.forms import AuthorForm
from blog.models import Author
# Create your views here.


def home(request):
    return HttpResponse('Blog home page.')


def author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            # a = Author.objects.create(**form.cleaned_data)
            # a.save()
            form.save()
            return HttpResponseRedirect('/blog/author/')
    p_data = Author.objects.all()
    form = AuthorForm()
    return render(request, 'author.html', {'author_form': form, 'p_data': p_data})

