from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, InlinePanel, FieldRowPanel
from wagtail.fields import RichTextField, StreamField

from modelcluster.fields import ParentalKey
from base.models import AboutPage
from investments.models import InvestmentsPage
from strategies.models import StrategyPage


class HomePage(Page):
    # ********************* Hero Section ***********************
    hero_heading_one = models.CharField(
        verbose_name="Hero Heading One",
        max_length=255,
        blank=True,
        null=True,
        help_text="Provide a descriptive heading for the hero section that introduces and summarizes the business.",
    )
    hero_heading_two = models.CharField(
        verbose_name="Hero Heading Two",
        max_length=255,
        blank=True,
        null=True,
        help_text="Provide a descriptive heading for the hero section that introduces and summarizes the business.",
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name="Hero Image",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Choose an image to visually represent the hero section, capturing attention and conveying the essence of the business.",
    )
    hero_cta_text = models.CharField(
        verbose_name=" Call-to-Action Text",
        max_length=255,
        null=True,
        blank=True,
        help_text="Enter the text to display on the Call-to-Action (CTA) button in the hero section.",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Call-to-Action Link",
        help_text="Choose a page to link to when the CTA button in the hero section is clicked.",
    )

    page_description = 'Homepage for Scipio Holding Investment Group featuring a hero section, \
         "About Scipio Holding," "Strategies," and "Investments" tabs. These tabs mirror \
            independent pages: StrategyPage, AboutPage, and InvestmentsPage.'

    content_panels = Page.content_panels + [
        # *********** Hero Section **************
        MultiFieldPanel(
            [
                MultiFieldPanel(
                    [
                        FieldPanel("hero_image"),
                        FieldPanel("hero_heading_one"),
                        FieldPanel("hero_heading_two"),
                    ],
                    heading="Hero Content",
                    help_text="Customize the visual and textual components of the Hero section. Upload an image, provide a welcome message, a heading, and a subheading.",
                ),
                MultiFieldPanel(
                    [
                        FieldPanel("hero_cta_text"),
                        FieldPanel("hero_cta_link"),
                    ],
                    heading="Hero CTA",
                    help_text="Configure the call-to-action (CTA) button for the Hero section. Specify the text and link for the CTA button.",
                ),
            ],
            heading="Hero Section",
            help_text="Customize the content for the Hero section. Include an image, welcome text, heading, subheading, call-to-action (CTA) text, and CTA link.",
        ),
    ]

    def aboutpage_content(self):
        aboutpage = AboutPage.objects.filter(live=True).first()
        return aboutpage

    def investments_page_content(self):
        investments_page = InvestmentsPage.objects.filter(live=True).first()
        return investments_page

    def strategy_page_content(self):
        strategy_page = StrategyPage.objects.filter(live=True).first()
        return strategy_page

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context["aboutpage_content"] = self.aboutpage_content()
        context["investments_page_content"] = self.investments_page_content()
        context["strategy_page_content"] = self.strategy_page_content()
        return context
