# Generated migration to add is_new_employee field to auth.User

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE auth_user ADD COLUMN is_new_employee BOOLEAN DEFAULT FALSE;',
            reverse_sql='ALTER TABLE auth_user DROP COLUMN is_new_employee;',
        ),
    ]
