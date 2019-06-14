# Generated by Django 2.2 on 2019-06-14 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг ответа'),
        ),
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.TextField(default='', verbose_name='Тело ответа'),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рэйтинг вопроса'),
        ),
        migrations.AddField(
            model_name='tag',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рэйтинг тэга'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации ответа'),
        ),
        migrations.AlterField(
            model_name='like',
            name='type',
            field=models.CharField(choices=[('Like', '+'), ('Dislike', '-')], default='+', max_length=2),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='questions.Profile'),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания вопроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(default='', verbose_name='Тело вопроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(default='', max_length=128, verbose_name='Заголовок вопроса'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(default='', max_length=64, unique=True, verbose_name='Имя тэга'),
        ),
    ]
