from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_qrorder_qrorderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Phần trăm'), ('fixed', 'Số tiền cố định')], max_length=10)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('max_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_to', models.DateTimeField()),
                ('max_uses', models.IntegerField(default=1)),
                ('times_used', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='qrorder',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='qrorder',
            name='original_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='qrorder',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Coupon'),
        ),
    ]
