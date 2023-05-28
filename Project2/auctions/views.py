from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from .models import User, Listing, Comment, Category, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_closed=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class new_listing_form(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "image", "category"]

@login_required()
def create_listing(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = new_listing_form(request.POST, request.FILES)
            #create a new listing
            if form.is_valid():
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                price = form.cleaned_data["price"]
                image = form.cleaned_data.get("image")
                category = form.cleaned_data["category"]
                creator = request.user

                listing = Listing(title=title, description=description, price=price, image=image, category=category, creator=creator)
                listing.save()

                return HttpResponseRedirect(reverse("view_listing", kwargs={"id": listing.id}))
            else:
                return render(request, "auctions/create.html", {
                    "form": form,
                    "message": "Invalid listing, please try again."
                })
        else:
            return render(request, "auctions/create.html", {
                "form": new_listing_form()
            })
    else:
        return render(request, "auctions/create.html", {
            "message": "Please log in to create your listing."
        })

class new_bid_form(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]

@login_required
def view_listing(request, id):
    listing = Listing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing)
    highest_bid = bids.order_by('-price').first()
    num_bids = len(bids)

    if request.method == 'POST':
        if 'watchlist' in request.POST:
            #add/remove listing to/from watchlist
            listing = Listing.objects.get(pk=id)

            if listing in request.user.watchlist.all():
                request.user.watchlist.remove(listing)
            else:
                request.user.watchlist.add(listing)

        elif 'bid' in request.POST:
            #add bid for listing if higher than price/existing highest bids
            form  = new_bid_form(request.POST)

            if form.is_valid():
                price = form.cleaned_data["price"]

                if price >= listing.price:
                    if num_bids > 0 and price > highest_bid.price:
                        new_bid = Bid(price=price, listing=listing, bidder=request.user)
                        new_bid.save()

                        return HttpResponseRedirect(reverse("view_listing", kwargs={"id": listing.id}))

                    elif num_bids == 0:
                        new_bid = Bid(price=price, listing=listing, bidder=request.user)
                        new_bid.save()

                        return HttpResponseRedirect(reverse("view_listing", kwargs={"id": listing.id}))

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": comments,
                "highest_bid": highest_bid,
                "message": "Bid price too low!",
                "form": form
            })

        elif 'comment' in request.POST:
            #add comment to listing
            content = request.POST.get('content')
            comment = Comment(content=content, listing=listing, commenter=request.user)
            comment.save()

        elif 'close_listing' in request.POST:
            #close listing

            if num_bids == 0:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "highest_bid": highest_bid,
                    "form": new_bid_form(),
                    "message": "No bids for this listing yet!"
                })

            listing.is_closed = True
            listing.save()

        elif 'delete' in request.POST:
            #delete listing
            listing.delete()
            return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("view_listing", kwargs={"id": listing.id}))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "highest_bid": highest_bid,
            "form": new_bid_form()
        })

def view_categories(request):
    objects = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": objects
    })

def view_category(request, name):
    category = Category.objects.get(name=name)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "name": name
    })

@login_required
def watchlist(request, id):
    return render(request, "auctions/index.html", {
        "listings": list(request.user.watchlist.all()),
        "name": "My Watchlist"
    })

@login_required
def my_listings(request, id):
    return render(request, "auctions/index.html", {
        "listings": list(request.user.listings.all()),
        "name": "My Listings"
    })

import itertools

@login_required
def my_bids(request, id):
    bids = list(Bid.objects.filter(bidder=request.user))
    listings=[]
    for bid in bids:
        listings.append(bid.listing)

    return render(request, "auctions/index.html", {
        "listings": listings,
        "name": "My Bids"
    })
