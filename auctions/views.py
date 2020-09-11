from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from django.utils.datastructures import MultiValueDictKeyError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import User,Category,List,Bid,Comment,Watchlist
from decimal import Decimal
import imghdr
from math import *

def index(request):
    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    list =List.objects.all().filter(active=True).order_by('-id')[:5]

    context = {
        "categories": Category.objects.all().order_by('category'),
        "cart": cart,
        "count": count,
        "list": list
    }
    return render(request, "auctions/index.html",context)


def login_view(request):

    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

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
                "message": "Invalid username and/or password.", 
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })
    else:
        context = {
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    context = {
        "categories": Category.objects.all().order_by('category'),
        "cart": cart,
        "count": count
    }
    if request.method == "POST":
        last = ''
        first = request.POST["first"]
        last = request.POST["last"]
        username = request.POST["username"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        try:
            image = request.FILES["images"]
        except MultiValueDictKeyError:
            image = ''
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if not first.isalpha():
            return render(request, "auctions/register.html", {
                "message": "First Name contains only letters.",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })

        if not last=='':
            if not last.isalpha():
                check=True
                return render(request, "auctions/register.html", {
                    "message": "Last Name contains only letters.",
                    "categories": Category.objects.all().order_by('category'),
                    "cart": cart,
                    "count": count
                })
    
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })

        if not image=='':
            check_image = imghdr.what(image)
            if not (check_image== "jpg" or check_image== "jpeg" or check_image== "png"):
                return render(request, "auctions/register.html", {
                    "message": "jpg or png files are accepted.",
                    "categories": Category.objects.all().order_by('category'),
                    "cart": cart,
                    "count": count
                }) 

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,first_name = first,last_name = last,gender=gender,phone=phone,address=address,image=image)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })
        return render(request, "auctions/login.html", context)
    else:
        return render(request, "auctions/register.html", context)


@login_required(login_url = 'login')
def create(request):

    user = None
    cart = ''
    count='' 
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["imageurl"]
        currentbid = "No Bid"
        finalbid = 0.00
        active = True
        close = False
        category1 = request.POST["category"]
        category = Category.objects.get(category = category1)

        try:
            imageupload = request.FILES["imageupload"]
        except MultiValueDictKeyError:
            imageupload = ''

        try:
            startbid = float(request.POST["price"])
        except ValueError:
            return render(request, "auctions/create.html", {
                "message": "Please enter a valid price",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })
        
        if startbid > 10000.00:
            return render(request, "auctions/create.html", {
                "message": "Please put price below $10000",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })

        if not imageupload=='':
            check_image = imghdr.what(imageupload)
            if not (check_image== "jpg" or check_image== "jpeg" or check_image== "png"):
                return render(request, "auctions/create.html", {
                    "message": "jpg or png files are accepted.",
                    "categories": Category.objects.all().order_by('category'),
                    "cart": cart,
                    "count": count
                })
        try:
            if not url=='':
                URLValidator()(url)
        except ValidationError:
            return render(request,"auctions/create.html",{
                "message": "Please provide a valid url",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })

        if not imageupload=='' and not url=='':
            return render(request,"auctions/create.html",{
                "message": "Please choose any of one choice to upload image",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })

        currentbid = startbid
        # Attempt to create new list
        try:
            list = List(user= user, title = title, description = description, category = category, startbid =startbid, 
                        image = imageupload, url = url, currentbid = currentbid, finalbid = finalbid, active = active, close = close)
            list.save()
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Title/descriptions are already taken.",
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })
        success = "Successfully Cretaed a <b style=\"color:red;\">\"" + title + "\"</b> List in a <b style=\"color:red;\">\"" + category1 + "\"</b> Category"
        return render(request, "auctions/create.html",{
                "success": success,
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            })
    else:
        list = List.objects.all().filter(user=user).order_by('-id')
        context = {
            "list": list,
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
        return render(request, "auctions/create.html",context)

def active(request):
    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()


    context = {
        "allLists": List.objects.all().filter(active=True).order_by('id').reverse,
        "categories": Category.objects.all().order_by('category'),
        "cart": cart,
        "count": count
    }
    return render(request,"auctions/list.html",context)

def allList(request,category):
    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    category = category
    try:
        listall = Category.objects.get(category=category)
    except Category.DoesNotExist:
        if category == "All":
            lists = List.objects.all().order_by('id').reverse
        elif category == "under $50":
            lists = List.objects.all().filter(startbid__lt=50).order_by('-id')
        else:
            raise Http404("List does not Exist")
    
    if not category == "All":
        if not category=="under $50":
            lists = List.objects.all().filter(category=listall).order_by('id').reverse
    context = {
        "categories": Category.objects.all().order_by('category'),
        "allLists":lists,
        "cart": cart,
        "count": count
    }
    return render(request,"auctions/list.html",context)


@login_required(login_url='/login')
def fullList(request,title):
    cart = ''
    count=''
    if request.user.is_authenticated:
        name = request.user.username
        name =User.objects.get(username = name)
        cart = Bid.objects.all().filter(participant=name, selected=True)
        count = Bid.objects.all().filter(participant=name, selected=True).count()


    try:
        list = List.objects.get(title = title)
        comment = Comment.objects.all().filter(comments=list).order_by('id').reverse
    except List.DoesNotExist:
        raise Http404("List does not exist")

    watchhistory = Watchlist.objects.all().filter(name=name).filter(watchlist=list).order_by('id')[:1]
    context = {        
        "categories": Category.objects.all().order_by('category'),
        "lists":list,
        "watch" : watchhistory,
        "comment":comment,
        "cart": cart,
        "count": count
    }

    if request.method == "POST":

        if 'watchlist' in request.POST:
            watchedList_id = request.POST["watchid"]
            watchedList = List.objects.get(id = watchedList_id)
            watched = True

            try:
                check_watch = Watchlist.objects.get(name=name,watchlist=watchedList)

                context = {  
                    "message" : "You already saved as a wishlist", 
                    "categories": Category.objects.all().order_by('category'),
                    "lists":list ,
                    "watch" :watchhistory,
                    "comment":comment,
                    "cart": cart,
                    "count": count
                }
                return render(request,"auctions/fulllist.html",context)

            except Watchlist.DoesNotExist:
                watch =Watchlist(name=name,watchlist=watchedList,watched=watched)            
                watch.save()
                
            watchhistory = Watchlist.objects.all().filter(name=name).filter(watchlist=list)[:1]
            return render(request, "auctions/fulllist.html", {
                "categories": Category.objects.all().order_by('category'),
                "lists":watchedList ,
                "watch" :watchhistory,
                "comment":comment,
                "cart": cart,
                "count": count
            })

        elif 'bid' in request.POST:
            get_List = List.objects.get(title = title)
            start_bid = get_List.startbid
            current_bid =get_List.currentbid

            price = 0.00
            try:
                price = float(request.POST["dollar"])
            except ValueError:
                return render(request, "auctions/fulllist.html", {
                    "message": "Please enter a valid price",
                    "categories": Category.objects.all().order_by('category'),
                    "lists":get_List ,
                    "watch" :watchhistory,
                    "comment":comment,
                    "cart": cart,
                    "count": count
                })

            current = request.POST['current']

            if not current =="No Bid":
                current = current[2:]
                current = Decimal(current)
            else:
                current = start_bid

            current_now =current + 1
            current_now =floor(current_now)

            if price < current_now :
                current_now =str(current_now)
                message = "Please Enter US $ " +  current_now +  " or more"
                return render(request, "auctions/fulllist.html", {
                    "message": message,
                    "categories": Category.objects.all().order_by('category'),
                    "lists":get_List ,
                    "watch" :watchhistory,
                    "comment":comment,
                    "cart": cart,
                    "count": count
                })

            try:
                bid =Bid(lists=list, participant=name, bid=price)
                get_List.currentbid = price
            except IntegrityError:
                return render(request, "auctions/fulllist.html", {
                    "message": "You already placed with this amount",
                    "categories": Category.objects.all().order_by('category'),
                    "lists":get_List ,
                    "watch" :watchhistory,
                    "comment":comment,
                    "cart": cart,
                    "count": count
                })
            
            bid.save()
            get_List.save()
            
            watchhistory = Watchlist.objects.all().filter(name=name).filter(watchlist=list)
            message = "You are Successfully placed an amount $ " + str(price)  
            context = {  
                "success" : message, 
                "categories": Category.objects.all().order_by('category'),
                "lists":get_List ,
                "watch" :watchhistory,
                "comment":comment,
                "cart": cart,
                "count": count
            }
            return render(request,"auctions/fulllist.html",context)

        elif 'comment' in request.POST:
            list = List.objects.get(title=title)
            comment=request.POST["description"]
            
            commented = Comment(name=name, comments=list, comment=comment)
            commented.save()

            comment = Comment.objects.all().filter(comments=list).order_by('id').reverse
            watchhistory = Watchlist.objects.all().filter(name=name).filter(watchlist=list)

            context = {  
                "success" : "You successfully commented!", 
                "categories": Category.objects.all().order_by('category'),
                "lists":list ,
                "watch" :watchhistory,
                "comment":comment,
                "cart": cart,
                "count": count
            }
            return render(request,"auctions/fulllist.html",context)


    return render(request,"auctions/fulllist.html", context)


@login_required(login_url='/login')
def watchlist(request,username):
    cart = ''
    count=''
    users = username
    if request.user.is_authenticated:
        name = request.user.username
        user =User.objects.get(username = name)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    if not users == name:
        message = "No Grand Permission to access watchlist of " + users
        context = {  
            "message" : message, 
            "access" :"true",
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
        return render(request, "auctions/watchlist.html", context)
    else:
        get_name = User.objects.get(username=user)

    if request.method == "POST":
        if 'delete_watchlist' in request.POST:
            remove = request.POST["removed"]
                
            list = List.objects.get(title=remove)

            try:
                watchlist = Watchlist.objects.get(name=get_name, watchlist=list)
            except Watchlist.DoesNotExist:
                context ={
                    "message": "sorry List does not exist",
                    "categories": Category.objects.all().order_by('category'),
                    "watchlist": Watchlist.objects.all().filter(name=get_name).order_by('id').reverse,
                    "cart": cart,
                    "count": count
                }
                return render(request, "auctions/watchlist.html", context)


            message = "You are removed an item " + watchlist.watchlist.title
            watchlist.delete()
            context ={
                    "message": message,
                    "categories": Category.objects.all().order_by('category'),
                    "watchlist": Watchlist.objects.all().filter(name=get_name).order_by('id').reverse,
                    "cart": cart,
                    "count": count
                }
            return render(request, "auctions/watchlist.html", context)

    context = {
            "watchlist": Watchlist.objects.all().filter(name=get_name).order_by('id').reverse,
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url="/login")
def viewlist(request,username,title):
    cart = ''
    count=''
    users = username
    if request.user.is_authenticated:
        name = request.user.username
        user =User.objects.get(username = name)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()
    
    if not users == name:
        message = "No Grand Permission to access viewlist of " + users 
        context = {  
            "messages" : message, 
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
        return render(request, "auctions/viewlist.html", context)

    try:
        name = User.objects.get(username=name)
        list = List.objects.get(user=name,title=title)

    except List.DoesNotExist:
        raise http404("List does not exist")

    by_current = list.currentbid
    try:
        by_name = Bid.objects.get(lists=list,bid=by_current)
    except Bid.DoesNotExist:
        by_name =False

    bid = Bid.objects.all().filter(lists=list).order_by('id').reverse
    comment = Comment.objects.all().filter(comments=list).order_by('id').reverse
    
    if request.method == "POST":
        if 'close_list' in request.POST:
            titleclose = request.POST["titleclose"]
            currentclose = request.POST["currentclose"]
            winnerclose = request.POST["winnerclose"]

            try:
                update_list = List.objects.get(user=name, title=titleclose)
                
            except List.DoesNotExist:
                raise http404("list does not exist")

            
            update_bid = Bid.objects.get(lists=update_list, bid=currentclose)

            update_list.close = True
            update_list.active = False
            update_list.finalbid = currentclose
            update_list.winner = winnerclose

            update_bid.selected = True

            update_list.save();
            update_bid.save();
            list =List.objects.get(title=titleclose)
            
            cart = Bid.objects.all().filter(participant=name, selected=True)
            count = Bid.objects.all().filter(participant=name, selected=True).count()
            
            context = {
                "list" :list,
                "bid" : bid,
                "comment":comment,
                "categories": Category.objects.all().order_by('category'),
                "cart": cart,
                "count": count
            }
            return render(request,"auctions/viewlist.html", context)

        elif 'comment' in request.POST:
            list = List.objects.get(title=title)
            comment=request.POST["description"]
            
            commented = Comment(name=name, comments=list, comment=comment)
            commented.save()

            comment = Comment.objects.all().filter(comments=list).order_by('-id')

            context = {  
                "success" : "You successfully commented!", 
                "categories": Category.objects.all().order_by('category'),
                "list":list ,
                "bid" : bid,
                "comment":comment,
                "cart": cart,
                "count": count
            }
            return render(request, "auctions/viewlist.html", context)

    context = {
        "list" :list,
        "by_name":by_name,
        "bid" : bid,
        "comment":comment,
        "categories": Category.objects.all().order_by('category'),
        "cart": cart,
        "count": count
    }
    return render(request,"auctions/viewlist.html", context)
    
@login_required(login_url='/login')
def profile(request,username):
    cart = ''
    count=''
    if request.user.is_authenticated:
        user = request.user.username
        user =User.objects.get(username = user)
        cart = Bid.objects.all().filter(participant=user, selected=True)
        count = Bid.objects.all().filter(participant=user, selected=True).count()

    try:
        username = User.objects.get(username = username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    context = {
            "username": username,
            "categories": Category.objects.all().order_by('category'),
            "cart": cart,
            "count": count
        }
    return render(request, "auctions/profile.html", context)