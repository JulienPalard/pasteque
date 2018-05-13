from . import renderers
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Paste, Language
from .forms import PasteForm
from .tools import random_id
from webtools import settings


@csrf_exempt
def index(request):
    """Displays form."""
    data = {'menu': 'index',
            'max_characters': settings.PASTE['max_characters']}
    if request.method == 'POST':
        paste = Paste(slug=random_id(Paste),
                      paste_ip=request.META['REMOTE_ADDR'],
                      paste_agent=request.META['HTTP_USER_AGENT'])
        if request.FILES:
            for language_name, any_file in request.FILES.items():
                break
            language = Language.by_name(language_name)
            form = PasteForm({'language': language.id,
                              'title': any_file.name,
                              'private': settings.PASTE['private_by_default'],
                              'lifetime': settings.PASTE['default_lifetime'],
                              'content': any_file.read().decode()
                              }, instance=paste)
        else:
            form = PasteForm(request.POST, instance=paste)
        if not form.is_valid():
            data['form'] = form
            return render(request, 'paste/index.html', data)
        form.save() # Some logic added to overrided method, see forms.py
        location = request.build_absolute_uri(
            reverse('short_paste', kwargs={'slug': paste.slug}))
        return HttpResponseRedirect(location, content=location + "\n",
                                    content_type='text/plain')
    data['form'] = PasteForm(initial={
        'private': settings.PASTE['private_by_default'],
        'lifetime': settings.PASTE['default_lifetime'],
        'language': 14})
    data['absolute_index_url'] = request.build_absolute_uri(reverse('index'))
    return render(request, 'paste/index.html', data)


def show(request, slug, renderer='pygments'):
    """Display paste."""
    # Fetching object
    paste = get_object_or_404(Paste, slug=slug)
    data = {'title': paste.title,'slug': slug}
    # Handling expiration
    if paste.is_expired():
        return render(request, 'paste/expired.html')
    # Handling passwords
    if paste.password:
        if 'password' in request.POST:
            password = request.POST['password']
        elif 'password' in request.COOKIES:
            password = request.COOKIES['password']
        else:
            password = None
        if not paste.pwd_match(password):
            return render(request, 'paste/locked.html', data)
    # Before rendering actions
    paste.incr_viewcount()
    # Handling rendering modes
    if not renderer or renderer not in settings.PASTE['enabled_renderers']:
        renderer = settings.PASTE['default_renderer']
    data['current_renderer'] = renderer
    data['renderers'] = settings.PASTE['enabled_renderers']
    render_method = getattr(renderers, 'render_%s' % renderer)
    response = render_method(request, paste, data)

    # Responding
    if 'password' in request.POST:
        response.set_cookie('password', request.POST['password'])
    return response


def history(request):
    """Display last 25 public non-expired pastes."""
    pastes = Paste.objects.filter(private=False, expired=False).order_by('-pk')[:25]
    data = {'pastes': pastes, 'menu': 'history', 'default_renderer': settings.PASTE['default_renderer']}
    return render(request, 'paste/history.html', data)
