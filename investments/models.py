from django.db import models
from django_countries.fields import CountryField

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
    PreviewableMixin,
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
    search_fields = [
        index.SearchField('name')
    ]

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + []


    def get_preview_template(self, request, mode_name):
        return "investments/preview/policy.html"

    class Meta:
        verbose_name_plural = 'Investment Policies'
        verbose_name = 'Investment Policy'

class Acquistion(
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
        "Investor", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    # tags = TaggableManager()
    
    panels = [
        FieldPanel("name"),
        FieldPanel('country'),
        FieldPanel("date"),
        FieldPanel("descr"),
        FieldPanel("image"),
        FieldPanel("investor"),
        # FieldPanel('tags'),
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
        return "investments/preview/acquisition.html"


class Investor(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
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
        FieldPanel('image'),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
    ]

    def __str__(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + []

    def get_preview_template(self, request, mode_name):
        return "investments/preview/investor.html"


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
    role = models.CharField("Role", max_length=254, blank=True, null=True)
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
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("role"),
        FieldPanel("image"),
        FieldPanel("bio"),
        FieldPanel("country"),
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
        return "investments/preview/searcher.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        return context

    class Meta:
        verbose_name = "Searcher"
        verbose_name_plural = "Searchers"


class InvestmentSearcherRelationship(Orderable, models.Model):
    page = ParentalKey(
        "InvestmentsPage",
        related_name="investment_searcher_relationship",
        on_delete=models.CASCADE,
    )
    searcher = models.ForeignKey(
        "Searcher",
        related_name="searcher_investment_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("searcher")]


class InvestmentsPage(Page):
    tab_one_title = models.CharField(max_length=254,blank=True,null=True)
    tab_two_title = models.CharField(max_length=254,blank=True,null=True)
    tab_three_title = models.CharField(max_length=254,blank=True,null=True)
    subheading = models.TextField(blank=True)

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
            ],
            heading="Tab 2",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_three_title"),
                FieldPanel("subheading"),
                # InlinePanel("policies", heading="Policies", label="Policy"),
            ],
            heading="Tab 3",
        ),
    ]

    def searchers(self):
        return [
            n.searcher
            for n in self.investment_searcher_relationship.filter(
                searcher__live=True
            ).select_related("searcher")
        ]


    subpage_types = []

    def acquisitions(self):
        acquisitions = AcquistionPage.objects.filter(live=True)
        return acquisitions

    def policies(self):
        policies = InvestmentPolicy.objects.filter(live=True)
        return policies



class AcquistionTag(TaggedItemBase):
    content_object = ParentalKey(
        "AcquistionPage", related_name="aquisition_tags", on_delete=models.CASCADE
    )

class AcquistionListing(Page):
    intro = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]
    parent_page_types = ["home.HomePage"]
    subpage_types = ["AcquistionPage"]

    def get_context(self,request):
        context = super().get_context(request)
        acquisitions = AcquistionPage.objects.child_of(self).live()
        tag = request.GET.get('tag')
        if tag:
            acquisitions = acquisitions.filter(tags__name=tag)
        context['acquistions'] = acquisitions
        return context

    def acquisitions(self):
        acquisitions = AcquistionPage.objects.filter(live=True)
        return acquisitions

    def policies(self):
        policies = InvestmentPolicy.objects.filter(live=True)
        return policies


class AcquistionPage(Orderable,Page):
    acquistion = models.ForeignKey(
        "Acquistion", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    tags = ClusterTaggableManager(through=AcquistionTag, blank=True)

    @property
    def get_tags(self):
        tags = self.tags.all()
        base_url = self.get_parent().url
        for tag in tags:
            tag.url = f"{base_url}tags/{tag.slug}/"
        return tags

    content_panels = Page.content_panels + [
        FieldPanel("acquistion"),
        FieldPanel("tags"),
    ]

    parent_page_types = [AcquistionListing]
    subpage_types = []
