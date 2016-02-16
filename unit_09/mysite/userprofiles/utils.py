from django.core.exceptions import ImproperlyConfigured


try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

def get_form_class(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    # except ImportError, e: # python 2.7
    except ImportError as e: # python 3.4
        raise ImproperlyConfigured( 'Error loading module %s: "%s"' % (module, e))
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a form named "%s"' % (module, attr))
    return form
