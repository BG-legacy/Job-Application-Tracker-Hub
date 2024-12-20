from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ] 