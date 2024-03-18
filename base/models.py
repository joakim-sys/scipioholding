from django.db import models
from django import forms
from django.utils.translation import gettext as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
    MultipleChooserPanel,
)


from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    Page,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    TranslatableMixin,
    PreviewableMixin,
)

from wagtail.search import index

from .blocks import BaseStreamBlock


class AboutPage(Page):
    heading = models.CharField(
        'Subtitle',
        max_length=100,
        null=True,
        blank=True,
        help_text= 'Add a subtitle for this page. Example: "About Scopio Holding".'
    )
    tab_one_title = models.CharField(max_length=100, null=True, blank=True)
    tab_two_title = models.CharField(max_length=100, null=True, blank=True)
    tab_three_title = models.CharField(max_length=100, null=True, blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Upload an image to be displayed within the first tab.'
    )

    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Content",
        blank=True,
        use_json_field=True,
        help_text="Compose the content for this tab. Utilize various content blocks to structure and format the information effectively.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        MultiFieldPanel(
            [
                FieldPanel("tab_one_title"),
                FieldPanel("image"),
                FieldPanel("body"),
            ],
            heading="Customize content for Tab 1",
            help_text='Enter the title, upload an image, and compose the content for Tab 1. Use rich text formatting to enhance the presentation.'
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_two_title"),
                MultipleChooserPanel(
                    "aboutpage_team_relationship",
                    chooser_field_name="team_member",
                    heading="Team Members",
                    label="Member",
                    panels=None,
                ),
            ],
            heading="Customize content for Tab 2",
            help_text='Enter the title and select team members to feature in Tab 2. Team members can be added from the Team Menu => Members Snippet in the left sidebar.'
        ),
        MultiFieldPanel(
            [
                FieldPanel("tab_three_title"),
                MultipleChooserPanel(
                    "aboutpage_advisor_relationship",
                    chooser_field_name="advisor",
                    heading="Advisors",
                    label="Advisor",
                    panels=None,
                ),
            ],
            heading="Customize content for Tab 3",
            help_text='Enter the title and select advisors to feature in Tab 3. Advisors can be added from the Team Menu => Advisor Snippet in the left sidebar.'
        ),
    ]

    def team_members(self):
        return [
            n.team_member
            for n in self.aboutpage_team_relationship.filter(
                team_member__live=True
            ).select_related("team_member")
        ]

    def advisors(self):
        return [
            n.advisor
            for n in self.aboutpage_advisor_relationship.filter(
                advisor__live=True
            ).select_related("advisor")
        ]

    page_description  = 'This page allows you to showcase detailed information about Scipio Holding. It consists of three tabs, each focusing on different aspects. Mirrored on the homepage/landing page'


class StandardPage(Page):
    introduction = models.TextField(
        blank=True,
        null=True,
        help_text="Provide a brief introduction or overview for this page.",
    )
    body = StreamField(
        BaseStreamBlock(),
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
        help_text="Compose the main content for this page. Utilize various content blocks to structure and format the information effectively.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    page_description = "This page type allows you to create standard content pages with an introduction and a flexible body."


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):

    introduction = models.TextField(
        null=True,
        blank=True,
        help_text=" Provide a brief introduction or overview for this form page.",
    )
    body = StreamField(
        BaseStreamBlock(),
        use_json_field=True,
        verbose_name="Page Body",
        null=True,
        blank=True,
        help_text="Compose the main content for this form page using various content blocks.",
    )

    thank_you_text = RichTextField(
        verbose_name="Thank You Text",
        blank=True,
        help_text="Customize the message displayed to users after submitting the form.",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
        InlinePanel("form_fields", heading="Form fields", label="Field"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
                FieldPanel("subject"),
            ],
            heading="Email",
        ),
    ]

    page_description = "Create interactive forms with ease. Customize the page with images, introductions, and a flexible body. Manage form fields, set email notifications, and provide a personalized thank-you message."


class FooterLinkOne(models.Model):
    page = ParentalKey(
        "wagtailcore.Page", blank=True, null=True, on_delete=models.SET_NULL
    )


class FooterLinkTwo(models.Model):
    page = ParentalKey(
        "wagtailcore.Page", blank=True, null=True, on_delete=models.SET_NULL
    )


@register_snippet
class FooterInfo(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):
    footer_links_one_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Enter a title for the first links section in the footer.",
    )
    footer_links_two_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Enter a title for the first links section in the footer.",
    )
    subscribe_email_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Enter a title for the email subscription section in the footer.",
    )
    subscribe_email_body = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the text or body content for the email subscription section in the footer.",
    )

    footer_links_one = models.ManyToManyField(
        FooterLinkOne,
        blank=True,
        help_text="Add the links to display in Footer Links Column 1",
        related_name="links_one",
    )

    footer_links_two = models.ManyToManyField(
        FooterLinkTwo,
        blank=True,
        help_text="Add the links to display in Footer Links Column 2",
        related_name="links_two",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("footer_links_one_title"),
                FieldPanel("footer_links_one", widget=forms.CheckboxSelectMultiple),
            ],
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_links_two_title"),
                FieldPanel("footer_links_two", widget=forms.CheckboxSelectMultiple),
            ],
        ),
        FieldPanel("subscribe_email_title"),
        FieldPanel("subscribe_email_body"),
        PublishingPanel(),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Footer Information"
        verbose_name_plural = "Footer Information"

    def __str__(self):
        return "Footer Information"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {
            "footer_links_one_title": self.footer_links_one_title,
            "footer_links_two_title": self.footer_links_two_title,
            "footer_subscribe_email_title": self.subscribe_email_title,
            "footer_subscribe_email_body": self.subscribe_email_body,
        }


@register_setting
class SiteSettings(BaseSiteSetting):
    logo = models.CharField(
        verbose_name="Site Logo",
        max_length=20,
        help_text="Enter the text or name for the site logo. This text will be displayed as the logo in the header and footer.",
        default="Scipio",
    )
    branding_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="Scipio",
        verbose_name="Site Title",
        help_text='Enter the title to be displayed in the title tag of the website. If left blank, the default value is "Scipio."',
    )

    branding_welcome = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="Welcome to Scipio Holding Investment Group CMS",
        verbose_name="Welcome Text",
        help_text='Enter the welcome text to be displayed on the admin home page. If left blank, the default is "Welcome to Scipio CMS."',
    )
    branding_login = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="Sign in to Scipio",
        verbose_name="Login Text",
        help_text='Enter the text to be displayed on the login page. If left blank, the default is "Sign in to Scipio."',
    )


@register_setting
class GenericSettings(ClusterableModel, BaseGenericSetting):
    twitter_url = models.URLField("Twitter URL", blank=True, null=True)
    facebook_url = models.URLField("Facebook URL", blank=True, null=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    tiktok_url = models.URLField("Tiktok URL", blank=True, null=True)
    whatsapp_url = models.URLField("WhatsApp Business URL", blank=True, null=True)
    telegram_url = models.URLField("Telegram URL", blank=True, null=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True, null=True)

    email = models.CharField("Contact Email", max_length=100, blank=True, null=True)
    phone = models.CharField("Contact Phone", max_length=100, blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("twitter_url"),
                FieldPanel("facebook_url"),
                FieldPanel("instagram_url"),
                FieldPanel("tiktok_url"),
                FieldPanel("whatsapp_url"),
                FieldPanel("telegram_url"),
                FieldPanel("linkedin_url"),
            ],
            "Social Media URLs",
        ),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("phone"),
            ],
            "Email & Phone",
        ),
    ]
