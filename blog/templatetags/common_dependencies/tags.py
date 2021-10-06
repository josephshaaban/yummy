"""Collection of components that deliver common web development dependencies for templates"""
from django import template
from django.forms import MediaDefiningClass
from django.utils.safestring import mark_safe

register = template.Library()  # pylint: disable=C0103


@register.simple_tag(name="bootstrap4")
def component_dependencies_tag_bs4():
    """template tag to render components template dependencies"""
    return mark_safe(Bootstrap4().render_dependencies())


@register.simple_tag(name="jQuery")
def component_dependencies_tag_jq():
    """template tag to render components template dependencies"""
    return mark_safe(JQuery().render_dependencies())


@register.simple_tag(name="jQueryUI")
def component_dependencies_tag_jqui():
    """template tag to render components template dependencies"""
    return mark_safe(JQueryUI().render_dependencies())


class Bootstrap4(template.Node, metaclass=MediaDefiningClass):
    """Template tag for Bootstrap 4 dependency"""
    class Media:  # pylint: disable=R0903
        """Metaclass to define template dependencies"""
        css = {
            'all': [
                'blog/bootstrap/bootstrap-4.3.1-dist/css/bootstrap.min.css',
            ]
        }
        js = [
            'blog/bootstrap/bootstrap-4.3.1-dist/js/bootstrap.bundle.min.js',
        ]

    def render_dependencies(self):
        """ render dependencies, django renders based on css and js members in class Media"""
        # member media is defined in MediaDefiningClass
        return self.media.render()  # pylint: disable=E1101


class JQuery(template.Node, metaclass=MediaDefiningClass):
    """Template tag for jQuery dependency"""
    class Media:  # pylint: disable=R0903
        """Metaclass to define template dependencies"""
        css = {
            'all': [
            ]
        }
        js = [
            'blog/jquery_core/jquery-3.4.1-dist/jquery.min.js',
        ]

    def render_dependencies(self):
        """ render dependencies, django renders based on css and js members in class Media"""
        # member media is defined in MediaDefiningClass
        return self.media.render()  # pylint: disable=E1101


class JQueryUI(template.Node, metaclass=MediaDefiningClass):
    """Template tag for jQuery dependency"""
    class Media:  # pylint: disable=R0903
        """Metaclass to define template dependencies"""
        css = {
            'all': [
                'blog/jquery_ui/jquery-ui-1.12.1/jquery-ui.min.css',
                # 'blog/jquery_ui/jquery-ui-1.12.1/jquery-ui.structure.min.css',
                # 'blog/jquery_ui/jquery-ui-1.12.1/jquery-ui.theme.min.css',
            ]
        }
        js = [
            'blog/jquery_ui/jquery-ui-1.12.1/jquery-ui.min.js',
        ]

    def render_dependencies(self):
        """ render dependencies, django renders based on css and js members in class Media"""
        # member media is defined in MediaDefiningClass
        return self.media.render()  # pylint: disable=E1101
