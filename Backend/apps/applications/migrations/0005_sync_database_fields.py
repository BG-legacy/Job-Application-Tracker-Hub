from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('applications', '0004_alter_application_options_and_more'),
    ]

    operations = [
        # Rename company to company_name
        migrations.RenameField(
            model_name='application',
            old_name='company',
            new_name='company_name',
        ),

        # Add job_title field if missing
        migrations.AddField(
            model_name='application',
            name='job_title',
            field=models.CharField(default='Not Specified', max_length=255),
            preserve_default=False,
        ),

        # Update field types
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