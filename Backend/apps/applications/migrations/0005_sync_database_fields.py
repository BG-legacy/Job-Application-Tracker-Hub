from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0004_alter_application_options_and_more'),
    ]

    operations = [
        # Rename company to company_name (only if needed)
        migrations.RenameField(
            model_name='application',
            old_name='company',
            new_name='company_name',
        ),

        # Remove the job_title addition since it already exists
        migrations.AlterField(
            model_name='application',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[
                ('Pending', 'Pending'),
                ('Interview', 'Interview'),
                ('Offer', 'Offer'),
                ('Rejected', 'Rejected'),
                ('Accepted', 'Accepted'),
                ('Withdrawn', 'Withdrawn')
            ], default='Pending', max_length=20),
        ),
    ] 