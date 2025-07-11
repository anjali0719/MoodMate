import os
from jinja2 import Environment, FileSystemLoader, ChoiceLoader
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse


def get_app_template_dirs():
    """ Look into each app's 'templates/' directory """
    app_template_dirs = []
    for app in settings.INSTALLED_APPS:
        try:
            # app.__path__[0]  gives us the app dir
            mod = __import__(app)
            app_path = os.path.dirname(mod.__file__)
            template_path = os.path.join(app_path, 'templates')
            if os.path.isdir(template_path):
                app_template_dirs.append(template_path)

        except Exception:
            continue

    return app_template_dirs


def environment(**options):
    loaders = []

    # global shared templates
    if (settings.BASE_DIR / "jinja2_templates").exists():
        loaders.append(FileSystemLoader(str(settings.BASE_DIR / "jinja2_templates")))

    # per app templates
    app_dirs = get_app_template_dirs()
    if app_dirs:
        loaders.append(FileSystemLoader(app_dirs))

    # remove 'loader' from options if its there, to prevent duplicacy..
    options.pop('loader', None)
    
    env = Environment(
        loader=ChoiceLoader(loaders),
        **options
    )

    # add Django functions for static and reverse
    env.globals.update({
        'static': static,
        'url': reverse
    })

    return env
