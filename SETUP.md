# Getting started
Before making the contact form, first we need to setup the GRUG stack environment.

# Installing software

Installed via `pip`
1. django
2. django-htmx
3. django-tailwind
4. django-widget-tweaks

# Make new app
`python manage.py startapp core`

# Make static directory
Make a directory called `static` in the `core` app directory.
Make a directory called `core` in the `static` app directory (yes, really).

We'll use this directory later. Still more setup to do.

# Make templates directory
Make a directory called `templates` in the `core` app. 
Make a directory called `core` in the `templates` folder (stop asking questions, grug).

We'll use this directory later. Still more setup to do.

# Add to INSTALLED_APPS
```python
# Add these entries below the default Django applications
INSTALLED_APPS = [
    ...,
    'core',
    'django_htmx',
    'tailwind',
    'widget_tweaks',
]
```

# HTMX: Add Middleware
https://django-htmx.readthedocs.io/en/latest/installation.html
```python
MIDDLEWARE = [
    ...,
    "django_htmx.middleware.HtmxMiddleware",
    ...,
]
```

# HTMX: Download and add to static folder
1. Download HTMX [here](https://unpkg.com/htmx.org/dist/htmx.min.js)
2. Put it in the `core` app's static directory (you will put it in `core/static/core/htmx.min.js`)

We're done with HTMX for now.

# Tailwind: Create Tailwind CSS app
https://django-tailwind.readthedocs.io/en/latest/installation.html
`python manage.py tailwind init`

Follow instructions. Use default name `theme` for app.

# Tailwind: Modify `settings.py`
Add `theme` and `django_browser_reload` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...,
    'core',
    'django_htmx',
    'tailwind',
    'widget_tweaks',
    'theme',
    'django_browser_reload',
]
```
Register the `theme` app with the following line:

```python
TAILWIND_APP_NAME = 'theme'
```

Add `INTERNAL_IPS` setting:

```python
INTERNAL_IPS = [
    '127.0.0.1'
]
```

Add `django_browser_reload` middleware:

```python
MIDDLEWARE = [
    ...,
    'django_htmx.middleware.HtmxMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    ...,
]
```

# Tailwind: Install TailwindCSS dependencies
`python manage.py tailwind install`

# Tailwind: Add `django_browser_reload` to `urls.py`

```python
## contact/contact/urls.py

# Add 'include' to imports
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
```

When we created the `theme` app with `python manage.py tailwind init`, 
`django-tailwind` very kindly provided us a `base.html` file in the `theme/templates` folder.
Let's edit it.

# Final setup
The default `base.html` file provided by `django-tailwind` looks like this:

```html
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
	<head>
    <title>Django Tailwind</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
		{% tailwind_css %}
	</head>

	<body class="bg-gray-50 font-serif leading-normal tracking-normal">
		<div class="container mx-auto">
			<section class="flex items-center justify-center h-screen">
				<h1 class="text-5xl">Django + Tailwind = ❤️</h1>
			</section>
		</div>
	</body>
</html>
```

We need to add HTMX and _hyperscript to this file. Under `{% load static tailwind_tags %}`, add two more lines:

```html
{% load static %}
{% load django_htmx %}
```

Inside `<head>`, under `{% tailwind_css %}`, add:

```html
<script src="https://unpkg.com/hyperscript.org@0.9.7"></script>
<script src="{% static 'htmx.min.js' %}" defer></script>
```
This is the only install step for _hyperscript.

Your `base.html` file should look like this:

```html
{% load static tailwind_tags %}
{% load static %}
{% load django_htmx %}
<!DOCTYPE html>
<html lang="en">
	<head>
    <title>Django Tailwind</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
        
		{% tailwind_css %}
        <script src="https://unpkg.com/hyperscript.org@0.9.7"></script>
        <script src="{% static 'htmx.min.js' %}" defer></script>
	</head>

	<body class="bg-gray-50 font-serif leading-normal tracking-normal">
		<div class="container mx-auto">
			<section class="flex items-center justify-center h-screen">
				<h1 class="text-5xl">Django + Tailwind = ❤️</h1>
			</section>
		</div>
	</body>
</html>
```

Phew! Setup complete, grug brother. Time to rock and roll.

# Create view: `contact_page_view`

Open `core/views.py`. Erase everything and add this:

```python
from django.http import HttpResponse
from django.template import loader


def contact_page_view(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render({}, request))
```

Usually the `base.html` template won't be used directly. 

For now, we just want to check that everything is working fine.

# Add urls entries

In the `core` folder, make a file called `urls.py` and open it. Add the following:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.contact_page_view, name='contact_page'),
]
```

Open `contact/urls.py`. Modify `urlpatterns`:

```python
# Add the 'core' app 'urls.py' to the routing path.
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('core.urls')),
]
```

# Start your engines
We are ready to test to see if Tailwind is working.

Start the development server:
`python manage.py runserver`

Start Tailwind:
`python manage.py tailwind start`

Open `127.0.0.1:8000` in your browser. If everything works, you should see a page with the following:

`Django + Tailwind = ❤️`

# Create a template for `contact_page_view`
Like I said before, we usually don't use the `base.html` file directly. Instead, we create a Django template block that we extend later.

In `theme/templates`, open a new file called `contact_page.html` and add the following:

```html
{% extends 'base.html' %}

{% block content %}
    <h1>Hello from contact_page.html!</h1>
{% endblock %}
```

# Modify `contact_page_view`
Set the template for `contact_page_view` to `contact_page.html`

```python
def contact_page_view(request):
    template = loader.get_template('contact_page.html')
    return HttpResponse(template.render({}, request))
```

# Modify `base.html`
Remove the contents inside the `<body>` tag and add the following:

```html
<main id="main">
    {% block content %}{% endblock content %}
</main>
```

Save everything and the page should refresh (thanks, `django_browser_refresh`). At the very top left, it should read:

> Hello from contact_page.html!

When we go to `127.0.0.1:8000`, Django looks at `contact/urls.py` and finds that the index (the '' in path('', ...)) refers to `core/urls.py`.

In `core/urls.py`, the index is set to `views.contact_page_view`. 

The template for the view is `contact_page.html`, so Django looks in there.

`{% extends 'base.html' %}` tells Django that `contact_page.html` _inherits_ everything in the `base.html`.

`base.html` includes a Django template block, `{% block content %}{% endblock %}`. 
When a template extends `base.html` and includes a `{% block content %}{% endblock %}` block of its own, 
the contents inside that block will be sent to `base.html` and everything will be loaded up.

Any time you make a view for a new page, its template needs to include at least the following:

```html
{% extends 'base.html' %}

{% block content %}
    Your page content will go in here.
{% endblock %}
```

Understanding Django's template inheritance is important for this project.

This contact form will use HTMX to replace elements in the HTML (rather than replacing the whole page). 

In Django terms, we will be using template 'partials' to replace parts of a base contact form template.

But first, let's style a bit.

# A little styling with Tailwind
The contact page is unimpressive. Let's beautify it a bit with TailwindCSS.

In `base.html`, replace the opening `<body>` tag with the following:

```html
<!-- Changed bg-gray-50 to bg-gray-200 -->
<!-- Changed font-serif to font-sans -->
<body class="bg-gray-200 font-sans leading-normal tracking-normal">
```

Add some Tailwind classes to the `<main>` tag to center everything:
```html
<!-- Center everything -->
<main id="main" class="h-screen grid place-items-center">
```
Replace the `<h1>` tag and contents with the following:

```html
<h1 class="text-xl sm:text-6xl text-orange-600 font-bold">Contact Us</h1>
```

If you want to learn more about TailwindCSS, check out our guide.

[//]: # (TODO: Make guide and add link.)

Much better.

Now, 
