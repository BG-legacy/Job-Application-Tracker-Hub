# Generated by Django 4.2 on 2024-12-21 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teammember",
            name="role",
            field=models.CharField(
                choices=[("Admin", "Admin"), ("Member", "Member")], max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="teammember",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team_memberships",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="teammember",
            table=None,
        ),
        migrations.CreateModel(
            name="TeamTip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tips",
                        to="teams.team",
                    ),
                ),
                (
                    "upvotes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="upvoted_tips",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
