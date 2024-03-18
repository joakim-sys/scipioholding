from django.db import models
from django.utils.translation import gettext as _
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
)
from wagtail.search import index
from wagtail.fields import StreamField
from modelcluster.models import ClusterableModel, ParentalKey
from base.blocks import BaseStreamBlock


class AboutPageAdvisorRelationship(Orderable, models.Model):
    page = ParentalKey(
        "base.AboutPage",
        related_name="aboutpage_advisor_relationship",
        on_delete=models.CASCADE,
    )
    advisor = models.ForeignKey(
        "Advisor",
        related_name="advisor_aboutpage_relationship",
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel("advisor")]


class Advisor(
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
    role = models.CharField("Role", max_length=254)
    country = CountryField()
    linkedin_url = models.URLField("LinkedIn URL", null=True, blank=True)
    x_url = models.URLField("X URL", null=True, blank=True)

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
        FieldPanel("image"),
        FieldPanel("role"),
        FieldPanel("country"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("linkedin_url"),
                        FieldPanel("x_url"),
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
        index.FilterField("country"),
        index.AutocompleteField("first_name"),
        index.AutocompleteField("last_name"),
    ]

    @property
    def thumb_image(self):
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:
            return ""

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [
            # ("single_item", _("Single Item"))
        ]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_preview_template(self, request, mode_name):
        return "advisors/preview/advisor.html"

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        return context

    class Meta:
        verbose_name_plural = "Advisors"
