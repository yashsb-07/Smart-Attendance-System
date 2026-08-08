from django.db import migrations, models
import django.db.models.deletion


def create_roles_and_assign_existing_users(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    User = apps.get_model("accounts", "User")

    roles = {
        "super_administrator": Role.objects.create(
            name="super_administrator",
        ),
        "institution_administrator": Role.objects.create(
            name="institution_administrator",
        ),
        "faculty": Role.objects.create(
            name="faculty",
        ),
        "student": Role.objects.create(
            name="student",
        ),
    }

    users_without_role = User.objects.all()

    for user in users_without_role:
        if user.is_superuser:
            user.role_id = roles["super_administrator"].id
            user.save(update_fields=["role"])
            continue

        raise RuntimeError(
            "Step 2.2 migration found an existing non-superuser without "
            "a role. The migration was stopped to avoid assigning an "
            "unsupported role automatically. Assign an approved role "
            "to the existing user before rerunning this migration."
        )


def remove_roles(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    Role.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_managers_alter_user_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            (
                                "super_administrator",
                                "Super Administrator",
                            ),
                            (
                                "institution_administrator",
                                "Institution Administrator",
                            ),
                            (
                                "faculty",
                                "Faculty",
                            ),
                            (
                                "student",
                                "Student",
                            ),
                        ],
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Role",
                "verbose_name_plural": "Roles",
                "db_table": "roles",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="users",
                to="accounts.role",
            ),
        ),
        migrations.RunPython(
            create_roles_and_assign_existing_users,
            reverse_code=remove_roles,
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="users",
                to="accounts.role",
            ),
        ),
    ]