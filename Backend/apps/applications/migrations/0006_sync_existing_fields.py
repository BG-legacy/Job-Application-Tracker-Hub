from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0005_sync_database_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],  # No database operations needed
            state_operations=[
                migrations.AlterField(
                    model_name='application',
                    name='job_description',
                    field=models.TextField(),
                ),
                migrations.AddField(
                    model_name='application',
                    name='position',
                    field=models.CharField(max_length=200),
                ),
            ],
        ),
    ]