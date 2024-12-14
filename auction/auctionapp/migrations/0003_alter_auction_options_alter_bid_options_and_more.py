# Generated by Django 5.1.3 on 2024-12-13 22:38

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0002_item_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'verbose_name': 'Auction', 'verbose_name_plural': 'Auctions'},
        ),
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-bid_time']},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-start_time'], 'verbose_name': 'Auction Item', 'verbose_name_plural': 'Auction Items'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-payment_date'], 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AlterModelOptions(
            name='watchlist',
            options={'ordering': ['-added_on']},
        ),
        migrations.AddField(
            model_name='auction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='base_price',
            field=models.DecimalField(decimal_places=2, help_text='Minimum starting price', max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='auction',
            name='bid_increment',
            field=models.DecimalField(decimal_places=2, help_text='Minimum bid increment', max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='auction',
            name='item',
            field=models.OneToOneField(help_text='Item being auctioned', on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auctionapp.item'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='max_bidders',
            field=models.PositiveIntegerField(default=100, help_text='Maximum number of bidders allowed'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount of the bid', max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(help_text='Item being bid on', on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctionapp.item'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(help_text='User placing the bid', on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='bid_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of bids placed'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, help_text='Detailed description of the item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='highest_bid',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Highest bid for the item', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, help_text='Item image', null=True, upload_to='item_images/'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(help_text='Name of the item', max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(help_text='User who owns the item', on_delete=django.db.models.deletion.CASCADE, related_name='owned_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Starting price of the item', max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, help_text='Amount paid', max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='auction',
            field=models.OneToOneField(help_text='Auction being paid for', on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='auctionapp.auction'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('credit', 'Credit Card'), ('debit', 'Debit Card'), ('paypal', 'PayPal'), ('bank', 'Bank Transfer')], help_text='Payment method used', max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(help_text='User making the payment', on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Upload a profile picture', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='item',
            field=models.ForeignKey(help_text='Item being watched', on_delete=django.db.models.deletion.CASCADE, related_name='watchers', to='auctionapp.item'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.ForeignKey(help_text='User watching the item', on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='bid',
            unique_together={('item', 'user', 'bid_amount')},
        ),
        migrations.AlterUniqueTogether(
            name='watchlist',
            unique_together={('user', 'item')},
        ),
    ]