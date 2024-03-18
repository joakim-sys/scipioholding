from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from advisors.models import Advisor
from .models import Team


class TeamSnippetViewSet(SnippetViewSet):
    model = Team
    menu_label = 'Members'
    icon = 'group'
    list_display = ('first_name','last_name','job_title','thumb_image')
    list_filter = {
        "job_title": ["icontains"],
    }


class AdvisorSnippetViewSet(SnippetViewSet):
    model = Advisor
    menu_label = 'Advisors'
    icon = 'group'


class TeamSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = 'Team'
    menu_icon = 'group'
    menu_order = 300
    items = (TeamSnippetViewSet,AdvisorSnippetViewSet)


register_snippet(TeamSnippetViewSetGroup)
