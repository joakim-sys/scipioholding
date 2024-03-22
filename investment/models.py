from django.db import models
from django_countries.fields import CountryField
from django import forms

from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
    Orderable,
)
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PublishingPanel,
    MultipleChooserPanel,
    InlinePanel,
)
from wagtail.search import index
from wagtail.fields import StreamField, RichTextField
from modelcluster.models import ClusterableModel, ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import Tag, TaggedItemBase
from taggit.managers import TaggableManager
from wagtail.models import (
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
)
from base.blocks import BaseStreamBlock


class InvestmentPolicy(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    index.Indexed,
    ClusterableModel,
):
    name = models.CharField(max_length=254)
    icon = models.CharField(max_length=254, null=True, blank=True)
    descr = RichTextField(
        blank=True,
        null=True,
        features=["bold", "italic", "link"],
    )

    def __str__(self):
        return self.name

    panels = [FieldPanel("name"), FieldPanel("icon"), FieldPanel("descr")]
    search_fields = [index.SearchField("name")]

    class Meta:
        verbose_name_plural = "Investment Policies"
        verbose_name = "Investment Policy"


class Acquisition(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    name = models.CharField(max_length=254, null=True)
    date = models.DateField(null=True)
    country = CountryField()
    descr = RichTextField(
        blank=True,
        null=True,
        features=["bold", "italic", "link"],
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    investor = models.ForeignKey(
        "Investor", related_name="+", null=True, blank=True, on_delete=models.SET_NULL,
    )

    a_tags = TaggableManager()

    panels = [
        FieldPanel("name"),
        FieldPanel("country"),
        FieldPanel("date"),
        FieldPanel("descr"),
        FieldPanel("image"),
        FieldPanel("investor",heading='Acquirer'),
        FieldPanel('a_tags')
    ]

    search_fields = [
        index.SearchField("name"),
        index.SearchField("investor"),
        index.SearchField("country"),
        index.FilterField("date"),
        index.FilterField("country"),
    ]

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + []

    def __str__(self):
        return self.name

    def get_preview_template(self, request, mode_name):
        return "investment/preview/acquisition.html"


class Investor(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    # PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    job_title = models.CharField(max_length=254, null=True, blank=True)
    biography = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldRowPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        FieldPanel("job_title"),
        FieldPanel("biography"),
        FieldPanel("image"),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
    ]

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    class Meta:
        verbose_name_plural = 'Acquirers'
        verbose_name = 'Acquirer'

class Searcher(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    role = models.CharField("Investment Name", max_length=254, blank=True, null=True)
    country = CountryField()
    linkedin_url = models.URLField("LinkedIn URL", null=True, blank=True)
    bio = RichTextField(
        blank=True,
        null=True,
        features=["bold", "italic", "link"],
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("role"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                    ]
                )
            ],
            "Name of Searcher",
        ),
        FieldPanel("country"),
        FieldPanel("image"),
        FieldPanel("bio"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("linkedin_url"),
                    ]
                )
            ],
            "Socials",
        ),
        PublishingPanel(),
    ]
    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("role"),
        index.AutocompleteField("first_name"),
        index.AutocompleteField("last_name"),
    ]

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + []

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_preview_template(self, request, mode_name):
        return "investment/preview/searcher.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        return context

    class Meta:
        verbose_name = "Searcher"
        verbose_name_plural = "Searchers"


class InvestmentSearcherRelationship(Orderable, models.Model):
    page = ParentalKey(
        "InvestmentPage",
        related_name="investment_searcher_relationship",
        on_delete=models.CASCADE,
    )
    searcher = models.ForeignKey(
        "Searcher",
        related_name="searcher_investment_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("searcher")]


class InvestmentAcquisitionRelationship(Orderable, models.Model):
    page = ParentalKey(
        "InvestmentPage",
        related_name="investments_acquisition_relationship",
        on_delete=models.CASCADE,
    )
    acquisition = models.ForeignKey(
        "Acquisition",
        related_name="acquisition_investments_relationship",
        on_delete=models.CASCADE,
    )

class InvestmentPolicyRelationship(Orderable, models.Model):
    page = ParentalKey(
        "InvestmentPage",
        related_name="investments_policy_relationship",
        on_delete=models.CASCADE,
    )
    policy = models.ForeignKey(
        "InvestmentPolicy",
        related_name="policy_investments_relationship",
        on_delete=models.CASCADE,
    )




class InvestmentPage(Page):
    tab_one_title = models.CharField(max_length=254, blank=True, null=True)
    tab_two_title = models.CharField(max_length=254, blank=True, null=True)
    tab_three_title = models.CharField(max_length=254, blank=True, null=True)
    subheading = models.TextField(blank=True,help_text='Displayed below the Investment Policy Page Tab under the Investment Section')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("tab_one_title"),
                MultipleChooserPanel(
                    "investment_searcher_relationship",
                    chooser_field_name="searcher",
                    heading="Searchers",
                    label="Searcher",
                    panels=None,
                ),
            ],
            heading="Tab 1",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_two_title"),
                MultipleChooserPanel(
                    "investments_acquisition_relationship",
                    chooser_field_name="acquisition",
                    heading="Acquisitions",
                    label="Acquisition",
                    panels=None,
                ),
            ],
            heading="Tab 2",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_three_title"),
                FieldPanel("subheading"),
                MultipleChooserPanel(
                    "investments_policy_relationship",
                    chooser_field_name="policy",
                    heading="Investment Policies",
                    label="Policy",
                    panels=None,
                    max_num=3
                ),
            ],
            heading="Tab 3",
        ),

    ]

    subpage_types = []

    def searchers(self):
        return [
            n.searcher
            for n in self.investment_searcher_relationship.filter(
                searcher__live=True
            ).select_related("searcher")
        ]

    def acquisitions(self):
        return [
            n.acquisition
            for n in self.investments_acquisition_relationship.filter(
                acquisition__live=True
            ).select_related("acquisition")
        ]

    def policies(self):
        return [
            n.policy
            for n in self.investments_policy_relationship.filter(
                policy__live=True
            ).select_related("policy")
        ]


