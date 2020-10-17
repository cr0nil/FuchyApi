# Generated by Django 3.1.1 on 2020-10-17 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fuchyRestApi.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fuchyRestApi', '0002_auto_20200924_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(validators=[fuchyRestApi.models.validate_message_content])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
