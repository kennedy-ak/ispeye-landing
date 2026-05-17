from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ApprovedEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Approved Email',
                'verbose_name_plural': 'Approved Emails',
                'ordering': ['email'],
            },
        ),
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('institution', models.CharField(blank=True, max_length=200)),
                ('reason', models.TextField()),
                ('status', models.CharField(
                    choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                    default='pending',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('reviewer_note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Access Request',
                'verbose_name_plural': 'Access Requests',
                'ordering': ['-created_at'],
            },
        ),
    ]
