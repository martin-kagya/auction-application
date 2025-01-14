from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = (
        ('Bidder', 'bidder'), 
        ('Seller', 'seller')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        help_text="Upload a profile picture"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Item(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the item")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        help_text="Starting price of the item"
    )
    image = models.ImageField(
        upload_to='item_images/', 
        blank=True, 
        null=True, 
        help_text="Item image"
    )
    highest_bid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Highest bid for the item"
    )
    bid_count = models.PositiveIntegerField(
        default=0, 
        help_text="Number of bids placed"
    )
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_items',
        help_text="User who owns the item"
    )
    description = models.TextField(
        blank=True, 
        help_text="Detailed description of the item"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    @property
    def time_remaining(self):
        now = timezone.now()
        if now > self.end_time:
            return None
        return self.end_time - now

    def save(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValueError("End time cannot be before or equal to start time")
        
        # Ensure highest_bid is not less than price
        if self.highest_bid and self.highest_bid < self.price:
            self.highest_bid = self.price
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Auction Item'
        verbose_name_plural = 'Auction Items'

class Bid(models.Model):
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='bids',
        help_text="Item being bid on"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bids',
        help_text="User placing the bid"
    )
    bid_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Amount of the bid"
    )
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.bid_amount} on {self.item.name}"

    class Meta:
        ordering = ['-bid_time']
        unique_together = ['item', 'user', 'bid_amount']

class Auction(models.Model):
    item = models.OneToOneField(
        Item, 
        on_delete=models.CASCADE, 
        related_name='auction',
        help_text="Item being auctioned"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Minimum starting price"
    )
    bid_increment = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Minimum bid increment"
    )
    max_bidders = models.PositiveIntegerField(
        default=100,
        help_text="Maximum number of bidders allowed"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction for {self.item.name}"

    def save(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValueError("End time cannot be before or equal to start time")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

class Watchlist(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='watchlist',
        help_text="User watching the item"
    )
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='watchers',
        help_text="Item being watched"
    )
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} is watching {self.item.name}"

    class Meta:
        unique_together = ['user', 'item']
        ordering = ['-added_on']

class Payment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='payments',
        help_text="User making the payment"
    )
    auction = models.OneToOneField(
        Auction, 
        on_delete=models.CASCADE, 
        related_name='payment',
        help_text="Auction being paid for"
    )
    amount_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Amount paid"
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    PAYMENT_METHODS = (
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer')
    )
    payment_method = models.CharField(
        max_length=50, 
        choices=PAYMENT_METHODS,
        help_text="Payment method used"
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.user.username} for {self.auction.item.name}"

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

# Signal to create UserProfile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)