# Generated by Django 4.2.9 on 2024-03-18 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_homepage_hero_cta_link_homepage_hero_cta_text_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="hero_heading_one",
            field=models.CharField(
                blank=True,
                help_text="Provide a descriptive heading for the hero section that introduces and summarizes the business.",
                max_length=255,
                null=True,
                verbose_name="Hero Heading One",
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="hero_heading_two",
            field=models.CharField(
                blank=True,
                help_text="Provide a descriptive heading for the hero section that introduces and summarizes the business.",
                max_length=255,
                null=True,
                verbose_name="Hero Heading Two",
            ),
        ),
    ]
