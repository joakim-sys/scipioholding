from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from base.blocks import BaseStreamBlock
from modelcluster.fields import ParentalKey


class Tab(models.Model):
    name = models.CharField(max_length=254)
    content = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )
    page = ParentalKey("StrategyPage", related_name="tabs", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    panels = [FieldPanel("name"), FieldPanel("content")]


class StrategyPage(Page):
    introduction = models.TextField(
        blank=True,
        null=True,
        help_text="Provide a brief introduction or overview for this page.",
    )
    tab_one_title = models.CharField(max_length=254,null=True,blank=True)
    tab_one_content = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )

    tab_two_title = models.CharField(max_length=254,null=True,blank=True)
    tab_two_content = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )

    tab_three_title = models.CharField(max_length=254,null=True,blank=True)
    tab_three_content = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )

    tab_four_title = models.CharField(max_length=254,null=True,blank=True)
    tab_four_content = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("tab_one_title"),
                FieldPanel("tab_one_content"),
            ],
            heading="Tab 1",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_two_title"),
                FieldPanel("tab_two_content"),
            ],
            heading="Tab 2",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_three_title"),
                FieldPanel("tab_three_content"),
            ],
            heading="Tab 3",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_four_title"),
                FieldPanel("tab_four_content"),
            ],
            heading="Tab 4",
        ),
    ]
