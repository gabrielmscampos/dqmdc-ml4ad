# Generated by Django 5.0.1 on 2024-01-17 10:00

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dqmio_file_indexer", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lumisection",
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
                ("ls_number", models.IntegerField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("oms_zerobias_rate", models.FloatField(blank=True, null=True)),
            ],
            options={
                "ordering": ["run__run_number", "ls_number"],
            },
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                (
                    "run_number",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                ("run_date", models.DateTimeField(blank=True, null=True)),
                ("year", models.IntegerField(blank=True, null=True)),
                ("period", models.CharField(blank=True, max_length=1, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("oms_fill", models.IntegerField(blank=True, null=True)),
                ("oms_lumisections", models.IntegerField(blank=True, null=True)),
                ("oms_initial_lumi", models.FloatField(blank=True, null=True)),
                ("oms_end_lumi", models.FloatField(blank=True, null=True)),
            ],
            options={
                "ordering": ["run_number"],
            },
        ),
        migrations.CreateModel(
            name="RunHistogram",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("primary_dataset", models.CharField(max_length=220)),
                ("path", models.CharField(max_length=220)),
                ("entries", models.BigIntegerField(null=True)),
                ("mean", models.FloatField(null=True)),
                ("rms", models.FloatField(null=True)),
                ("skewness", models.FloatField(null=True)),
                ("kurtosis", models.FloatField(null=True)),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="LumisectionHistogram1D",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("entries", models.IntegerField(blank=True, null=True)),
                (
                    "data",
                    django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, size=None),
                ),
                ("x_min", models.FloatField(blank=True, null=True)),
                ("x_max", models.FloatField(blank=True, null=True)),
                ("x_bin", models.IntegerField(blank=True, null=True)),
                (
                    "lumisection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_histograms",
                        to="dqmio_etl.lumisection",
                    ),
                ),
                (
                    "source_data_file",
                    models.ForeignKey(
                        blank=True,
                        help_text="Source data file that the specific Histogram was read from, if any",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s",
                        to="dqmio_file_indexer.fileindex",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Lumisection Histograms 1D",
            },
        ),
        migrations.CreateModel(
            name="LumisectionHistogram2D",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=220)),
                ("entries", models.IntegerField(blank=True, null=True)),
                (
                    "data",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=django.contrib.postgres.fields.ArrayField(
                            base_field=models.FloatField(), blank=True, size=None
                        ),
                        blank=True,
                        size=None,
                    ),
                ),
                ("x_min", models.FloatField(blank=True, null=True)),
                ("x_max", models.FloatField(blank=True, null=True)),
                ("x_bin", models.IntegerField(blank=True, null=True)),
                ("y_max", models.FloatField(blank=True, null=True)),
                ("y_min", models.FloatField(blank=True, null=True)),
                ("y_bin", models.IntegerField(blank=True, null=True)),
                (
                    "lumisection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_histograms",
                        to="dqmio_etl.lumisection",
                    ),
                ),
                (
                    "source_data_file",
                    models.ForeignKey(
                        blank=True,
                        help_text="Source data file that the specific Histogram was read from, if any",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s",
                        to="dqmio_file_indexer.fileindex",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Lumisection Histograms 2D",
            },
        ),
        migrations.AddConstraint(
            model_name="run",
            constraint=models.UniqueConstraint(fields=("run_number",), name="unique run number"),
        ),
        migrations.AddField(
            model_name="lumisection",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lumisections",
                to="dqmio_etl.run",
            ),
        ),
        migrations.AddField(
            model_name="runhistogram",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="histograms",
                to="dqmio_etl.run",
            ),
        ),
        migrations.AddField(
            model_name="runhistogram",
            name="source_data_file",
            field=models.ForeignKey(
                blank=True,
                help_text="Source data file that the specific Histogram was read from, if any",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s",
                to="dqmio_file_indexer.fileindex",
            ),
        ),
        migrations.AddConstraint(
            model_name="lumisectionhistogram1d",
            constraint=models.UniqueConstraint(
                fields=("lumisection", "title"),
                name="unique run / ls / 1d histogram combination",
            ),
        ),
        migrations.AddConstraint(
            model_name="lumisectionhistogram2d",
            constraint=models.UniqueConstraint(
                fields=("lumisection", "title"),
                name="unique run / ls / 2d histogram combination",
            ),
        ),
        migrations.AddConstraint(
            model_name="lumisection",
            constraint=models.UniqueConstraint(fields=("run", "ls_number"), name="unique run/ls combination"),
        ),
        migrations.AddConstraint(
            model_name="runhistogram",
            constraint=models.UniqueConstraint(
                fields=("run", "primary_dataset", "title"),
                name="unique run/dataset/histogram combination",
            ),
        ),
    ]
