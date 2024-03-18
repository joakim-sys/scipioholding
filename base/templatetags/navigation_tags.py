from django import template
from wagtail.models import Page, Site
from base.models import FooterInfo
from home.models import HomePage
from base.models import StandardPage

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()


@register.simple_tag(takes_context=False)
def is_active(page, current_page):
    return current_page.url_path.startswith(page.url_path) if current_page else False


@register.inclusion_tag("tags/top_menu.html", takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
    return {
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": context["request"],
    }


@register.inclusion_tag("tags/top_menu_children.html", takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    for menuitem in menuitems_children:
        menuitem.has_dropdown = has_menu_children(menuitem)
        menuitem.active = (
            calling_page.url_path.startswith(menuitem.url_path)
            if calling_page
            else False
        )
        menuitem.children = menuitem.get_children().live().in_menu()
    return {
        "parent": parent,
        "menuitems_children": menuitems_children,
        "request": context["request"],
    }


@register.inclusion_tag("tags/deep_dropdown_children.html", takes_context=True)
def deep_dropdown_children(context, parent, calling_page=None):
    deep_dropdown_children = parent.get_children().live().in_menu()
    for item in deep_dropdown_children:
        item.active = (
            calling_page.url_path.startswith(item.url_path) if calling_page else False
        )
    return {
        "parent": parent,
        "deep_dropdown_children": deep_dropdown_children,
        "request": context["request"],
    }


@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }


@register.inclusion_tag("base/include/footer_links_one_title.txt", takes_context=True)
def get_footer_links_one_title(context):
    footer_links_one_title = context.get("footer_links_one_title", "")
    if not footer_links_one_title:
        instance = FooterInfo.objects.first()
        footer_links_one_title = instance.footer_links_one_title if instance else "Scipio Holding"
    return {"footer_links_one_title": footer_links_one_title}

@register.inclusion_tag("base/include/footer_links_two_title.txt", takes_context=True)
def get_footer_links_two_title(context):
    footer_links_two_title = context.get("footer_links_two_title", "")
    if not footer_links_two_title:
        instance = FooterInfo.objects.first()
        footer_links_two_title = instance.footer_links_two_title if instance else "Legal"
    return {"footer_links_two_title": footer_links_two_title}



@register.inclusion_tag(
    "base/include/footer_subscribe_email_title.txt", takes_context=True
)
def get_footer_subscribe_email_title(context):
    footer_subscribe_email_title = context.get("footer_subscribe_email_title", "")
    if not footer_subscribe_email_title:
        instance = FooterInfo.objects.first()
        footer_subscribe_email_title = (
            instance.subscribe_email_title if instance else "Get in Touch"
        )
    return {"footer_subscribe_email_title": footer_subscribe_email_title}


@register.inclusion_tag(
    "base/include/footer_subscribe_email_body.txt", takes_context=True
)
def get_footer_subscribe_email_body(context):
    footer_subscribe_email_body = context.get("footer_subscribe_email_body", "")
    if not footer_subscribe_email_body:
        instance = FooterInfo.objects.first()
        footer_subscribe_email_body = (
            instance.subscribe_email_body
            if instance
            else "Get in touch with Scipio Holding Investment Group"
        )
    return {"footer_subscribe_email_body": footer_subscribe_email_body}


@register.inclusion_tag("base/include/footer_links_one.html", takes_context=True)
def get_footer_links_one(context):
    footer_links_one = context.get("footer_links_one", "")
    if not footer_links_one:
        instance = HomePage.objects.filter(live=True).first()
        footer_links_one = instance.get_children().in_menu() if instance else []
    return {"footer_links_one": footer_links_one}

@register.inclusion_tag("base/include/footer_links_two.html", takes_context=True)
def get_footer_links_two(context):
    footer_links_two = context.get("footer_links_two", "")
    if not footer_links_two:
        instance = StandardPage.objects.filter(live=True)
        footer_links_two = instance if instance else []
    return {"footer_links_two": footer_links_two}

