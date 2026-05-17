from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporter_name', models.CharField(max_length=150)),
                ('reporter_email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('steps_to_reproduce', models.TextField(blank=True)),
                ('severity', models.CharField(
                    choices=[
                        ('low', 'Low — Minor inconvenience'),
                        ('medium', 'Medium — Feature not working'),
                        ('high', 'High — App crashes'),
                        ('critical', 'Critical — Data loss / security issue'),
                    ],
                    default='medium',
                    max_length=20,
                )),
                ('app_version', models.CharField(blank=True, default='1.3.1', max_length=20)),
                ('device_model', models.CharField(blank=True, max_length=100)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='bug_reports/')),
                ('status', models.CharField(
                    choices=[
                        ('new', 'New'),
                        ('in_progress', 'In Progress'),
                        ('resolved', 'Resolved'),
                        ('wont_fix', "Won't Fix"),
                    ],
                    default='new',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin_notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Bug Report',
                'verbose_name_plural': 'Bug Reports',
                'ordering': ['-created_at'],
            },
        ),
    ]
