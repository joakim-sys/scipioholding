from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from .models import Searcher, Investor, Acquistion, InvestmentPolicy


class InvestmentPolicySnippetView(SnippetViewSet):
    model = InvestmentPolicy
    search_fields = ("name",)


class AcquistionSnippetView(SnippetViewSet):
    model = Acquistion
    ordering = ("date",)
    search_fields = ("name",)



class InvestorSnippetViewSet(SnippetViewSet):
    model = Investor
    search_fields = ("first_name", "last_name")


class SearcherSnippetViewSet(SnippetViewSet):
    model = Searcher
    menu_label = "Searchers"
    icon = "group"


class InvestmentSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = "Investments"
    menu_icon = "dollar"
    menu_order = 400
    items = (
        SearcherSnippetViewSet,
        InvestorSnippetViewSet,
        AcquistionSnippetView,
        InvestmentPolicySnippetView,
    )


register_snippet(InvestmentSnippetViewSetGroup)
