# Using the Grug Stack to Build a Hypermedia-Driven Application

The Grug Stack is a development environment used for
building [Hypermedia-Driven Applications](https://htmx.org/essays/hypermedia-driven-applications/).
HDA development is done in a powerful and modern REST API called HTML and is guided primarily by the principle
of [Locality of Behavior](https://htmx.org/essays/locality-of-behaviour/).

The Grug Stack is composed of:

1. Django (or some other back-end)
2. TailwindCSS
3. HTMX
4. _hyperscript (or Alpine.js if you prefer that)

And two django extensions:

1. django-widget-tweaks
2. django-render-block

This guide will provide an overview of how to build a simple HDA--a contact form with a confirmation step.

## Github

If you want to skip to the good parts, go to the [Github repo](https://github.com/mijokijo/grug_contact_form) for this
project. This guide only covers the key points in the application.

## Guide

HDAs use hypermedia like HTML as the [Engine of Application State](https://htmx.org/essays/hateoas/).
Consequently, the majority of the action in the contact form, both functionality and styling, is in the Django
templates.

The tree structure of the templates directory looks like this:

```
core
└── templates
    └── core
        ├── base.html
        ├── contact_page.html
        └── form
            ├── _confirmation.html
            ├── _send.html
            └── contact_form.html
```

This project simulates using the contact form on an actual page. The form is `{% included %}` on `contact_page.html`.

```html+django
<div id="contact-form">
    {% include 'core/form/contact_form.html' %}
</div>
```

`_send.html` is just a success message, so the action is in the other two templates.

## HTMX in Hypermedia-Driven Application Development

HTMX is a Javascript library that upgrades
the [REST API called HTML](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/). It allows
developers to manage complexity and build fast and secure front-ends with ease without touching Javascript.

In `contact_page.html`:

```html+django
<form>
    ...
    <button hx-post="confirm/"
            hx-target="#contact-form"
            hx-swap="innerHTML">
        Confirm
    </button>
</form>
```

The `hx-*` attributes are HTMX attributes.
When the form is submitted, a POST request is made to the `confirm` endpoint.
That returns the contents of `_confirmation.html`.
HTMX takes those contents and swaps the innerHTML of the element with id `#contact-form`, the div that wraps the form
in `contact_page.html` shown above.

## Working with Template Fragments

Modern web development involves delivering parts of a page, rather than a full page, on many user interactions.
The `django-render-block` extension allows developers to
deliver [template fragment](https://htmx.org/essays/template-fragments/) easily.

Our contact form has three states accessed through three views, but only one of them renders a full page.

```python
from render_block import render_block_to_string


def contact_page(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = ContactForm(request.POST)
        context = {'form': form}
        block = 'contact_form'
        html = render_block_to_string("core/contact_page.html", block, context)
        return HttpResponse(html)
    form = ContactForm()
    context = {'form': form}
    return render(request, 'core/contact_page.html', context)
```

On a GET request (like when clicking on a Contact Us link in a nav bar), `contact_page` will render the full page.
However, if it receives a POST request, it will render a template fragment using the `render_block_to_string` function.

`contact_page.html`

```html+django hl_lines="5 6"
{% extends 'core/base.html' %}

{% block content %}
    <h1>Contact Form</h1>
    {% block contact_form %}
        <div id="contact-form">
            {% include 'core/form/contact_form.html' %}
        </div>
    {% endblock %}
{% endblock %}
```

`views.py`

```python hl_lines="7 8"
from render_block import render_block_to_string

def contact_page(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = ContactForm(request.POST)
        context = {'form': form}
        block = 'contact_form'
        html = render_block_to_string("core/contact_page.html", block, context)
        return HttpResponse(html)
    form = ContactForm()
    context = {'form': form}
    return render(request, 'core/contact_page.html', context)
```

`contact_form.html`
```html+django hl_lines="5 6"
{% block contact_form %}
<form>
 ...
    <button hx-post="confirm/"
            hx-target="#contact-form"
            hx-swap="innerHTML">
        Confirm
    </button>
</form>
{% endblock %}
```

When the Confirm button is clicked, a request to the `confirm` endpoint is made.
The endpoint validates the form, and if valid, returns a confirmation template in our HTML API.
Otherwise, it returns the `contact_page` with the POST request.

In that case, `contact_page` will return only the contents of the `contact_form` block in the `contact_page.html`
template along with the context. HTMX will swap it into the innerHTML of the `#contact-form` div.

The `validate_then_confirm` and `send_form` views only return HttpResponses with the contents of the `contact_form`
block in their own templates.

Using `django-render-block` and HTMX, you have a direct pipeline to template fragments and a method for swapping the
fragment. All without writing a single line of Javascript.

So easy even a grug like me can do it.

While HTMX allows grugs like us to build modern web applications using an advanced REST API like HTML, TailwindCSS lets
us build modern designs directly in that same API.

That is the very essence of Hypermedia-Driven Application Development.

## TailwindCSS in Hypermedia-Driven Application Development

[TailwindCSS](https://tailwindcss.com/) is a set of utility classes that implement a design system.
HTML elements are styled locally, rather than having a 'semantic' class name that refers to style details in a CSS file
elsewhere.

In `contact_page.html`:

```html+django
{% load widget_tweaks %}
...
{% render_field field placeholder=field.label class="w-full bg-slate-200 font-normal font-body text-xl text-slate-900 border-2 border-slate-900 focus:ring-0 focus:outline-0 focus:border-cyan-500 placeholder:text-slate-500" %}
```

The `render_field` template tag is provided by `django-widget-tweaks`.
It allows us to style the form within the template, rather than being forced to style it in the form definition in
Python.

TailwindCSS utility classes and `django-widget-tweaks` allow developers to manage front-end complexity by putting all
styling information directly in our REST API.

## _hyperscript in Hypermedia-Driven Application Development

[_hyperscript](https://hyperscript.org/) is another Javascript library designed to help HDA developers build modern
front-ends while using HTML as the Engine of Application State. The cherry on top? We don't have to touch Javascript.

While HTMX handles HTTP requests and template fragment swapping, _hyperscript handles events and DOM manipulation.

This contact form uses it only once for a simple action: toggling a class on an HTML element and then removing another.

In `_confirmation.html`:

```html+django hl_lines="4"
<div id="buttons" class="flex flex-wrap justify-center gap-10">
    <button hx-target="#contact-form" hx-swap="innerHTML"
            hx-post="send/"
            _="on click toggle .hidden on #indicator then remove #buttons"
            class="max-w-fit px-14 py-4 bg-cyan-600 text-slate-100 text-2xl transition ease-in-out duration-300 hover:bg-cyan-600 cursor-pointer">
        Send
    </button>
    ...
</div>

<div id="indicator" class="hidden mx-auto">
    <svg id="L4" class="fill-cyan-500 mx-auto"
         ...
    </svg>
</div>
```

When a user clicks the Send button, _hyperscript toggles the `hidden` TailwindCSS utility class on the `#indicator`
element, a div with an SVG animation,
and then deletes the `#buttons` element.

_hyperscript is a small library, meaning you can use just a tiny bit of it like this without a large performance hit.
Although we don't use it much in the contact form, it allows HDA developers to localiz e all of our behavior in HTML, and
as such it is a respected member of the Grug Stack.

## Conclusion

If you are a full-stack developer in search of a technology stack that will uncomplicate your life while providing you
the features you need to build modern applications, the Grug Stack is for you.

If you want a guide on how to get the Grug Stack up and running, you may be interested
in [our guide](https://killianarts.online/en/articles/how-to-setup-a-grug-stack-development-environment/).