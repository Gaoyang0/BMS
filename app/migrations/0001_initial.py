# Generated by Django 2.0.6 on 2018-06-22 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('bname', models.CharField(db_index=True, max_length=32)),
                ('bprice', models.FloatField()),
                ('bstock', models.IntegerField()),
                ('bfamily', models.CharField(max_length=32)),
                ('bpic', models.CharField(max_length=64)),
            ],
        ),
    ]
