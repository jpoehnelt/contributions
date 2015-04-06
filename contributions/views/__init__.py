from contributions.settings import JINJA_ENVIRONMENT


def render_template(template, context=None):
    """
    Helper function for rendering templates with jinja.

    :param template: path to .html
    :param context: dictionary of values to pass to jinja
    :return: a rendered template
    """
    if context is None:
        context = {}
    return JINJA_ENVIRONMENT.get_template(template).render(context)
