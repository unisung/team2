# Generated by Django 3.1.3 on 2023-11-17 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Final', '0005_answer_voter_question_voter_alter_answer_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
