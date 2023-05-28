from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Bid(models.Model):
    price = models.PositiveIntegerField()
    listing = models.ForeignKey('Listing', blank=True, null=True, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return str(self.price)+" dollar Bid on "+self.listing.title+" by "+self.bidder.username

class Comment(models.Model):
    content = models.TextField(max_length=500)
    listing = models.ForeignKey('Listing', blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE, related_name="commenter")

    def __str__(self):
        return "Comment on "+self.listing.title+" posted by "+self.commenter.username

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="listing_images", blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="listing")
    creator = models.ForeignKey('User', null=True, on_delete=models.CASCADE, related_name="listings")
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " created by " + str(self.creator.username)

class User(AbstractUser, models.Model):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist_users")
    bids = models.ManyToManyField(Listing, blank=True, related_name="bid_users")

    def __str__(self):
        return self.username + str(self.id)
