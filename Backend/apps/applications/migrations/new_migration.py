from django.db import migrations, models

def copy_job_title_to_position(apps, schema_editor):
    Application = apps.get_model('applications', 'Application')
    for app in Application.objects.all():
        app.position = app.job_title
        app.save()

class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0009_application_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='position',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
        migrations.RunPython(copy_job_title_to_position),
    ] 