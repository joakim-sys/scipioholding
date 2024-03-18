# Generated by Django 4.2.9 on 2024-03-17 11:22

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("base", "0001_initial"),
        ("advisors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutpageadvisorrelationship",
            name="page",
            field=modelcluster.fields.ParentalKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="aboutpage_advisor_relationship",
                to="base.aboutpage",
            ),
        ),
    ]