from django.db import models
from django.utils.translation import gettext as _

from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
    Orderable
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


class AboutPageTeamMemberRelationship(Orderable, models.Model):
    page = ParentalKey(
        "base.AboutPage",
        related_name="aboutpage_team_relationship",
        on_delete=models.CASCADE,
    )
    team_member = models.ForeignKey(
        'Team', related_name="team_aboutpage_relationship", on_delete=models.CASCADE
    )

    panels = [FieldPanel("team_member")]



class Team(
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
    job_title = models.CharField("Job title", max_length=254)

    linkedin_url = models.URLField("LinkedIn URL", null=True, blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    bio = StreamField(
        BaseStreamBlock(), blank=True, verbose_name="biography", use_json_field=True
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
        FieldPanel("job_title"),
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
        FieldPanel("bio"),
        PublishingPanel(),
    ]
    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
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
        return 'team/preview/team-member.html'

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        return context

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
