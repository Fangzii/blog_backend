# Generated by Django 2.1.4 on 2019-02-20 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emotions_work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=32, verbose_name='文件名称')),
                ('file', models.FileField(blank=True, upload_to='uploadFile')),
                ('summarize', models.CharField(max_length=32, verbose_name='文件概述')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=32, verbose_name='图片名称')),
                ('image', models.ImageField(blank=True, upload_to='uploadImages', verbose_name='图片')),
                ('summarize', models.CharField(max_length=32, verbose_name='图片描述')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='emotions_work',
            name='file',
            field=models.ManyToManyField(to='emotions.File', verbose_name='文件'),
        ),
        migrations.AddField(
            model_name='emotions_work',
            name='image',
            field=models.ManyToManyField(to='emotions.Image', verbose_name='图片'),
        ),
    ]
