from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Posts, DateRequests, Dates
from django.contrib import messages
from authentication.models import Details
from django.contrib.auth.models import User



def home(request, username):
    user = request.user
    followers = DateRequests.objects.get(user=user)
    no_of_followers = followers.requests
    if not user.is_authenticated:
        return redirect("signup")
    user2 = get_object_or_404(User, username=user.username)
    if not Details.objects.filter(user=user).exists() :
        return redirect("details")
    details = Details.objects.get(user=user)
    fname = details.fname
    lname = details.lname
    relationship = details.relationship
    return render(
        request,
        "home/user.html",
        {
            "details": details,
            "fullname": fname + " " + lname,
            "relationship": relationship,
            "user": user2,
            "followers" : no_of_followers
        },
    )



def CreatePost(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("signup")
    if not Details.objects.filter(user=user).exists() :
        return redirect("details")
    if request.method == "POST":
        post = request.POST["post"]
        user = request.user
        Posts.objects.create(post=post, user=user)
        messages.success(request, "posted successfully")
        return redirect(feedSection)
    return render(request, "home/create.html")



def feedSection(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("signup")
    if not Details.objects.filter(user=user).exists() :
        return redirect("details")
    posts = Posts.objects.all().order_by("-created_at")

    # Prepare a list of posts with related user details
    posts_with_details = []
    for post in posts:
        # Fetch the details for each post's user
        details = Details.objects.filter(
            user=post.user
        ).first()  # Use .first() to avoid exceptions
        posts_with_details.append({"post": post, "details": details})

    return render(request, "home/feed.html", {"posts_with_details": posts_with_details})



def UserPosts(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("signup")
    username = user.username
    if not Details.objects.filter(user=user).exists() :
        return redirect("details")
    image_getter = Details.objects.get(user=user)
    images = image_getter.images
    posts = Posts.objects.filter(user=user).order_by("-created_at")
    return render(
        request,
        "home/userposts.html",
        {"post": posts, "user": username, "images": images},
    )


def SomeUser(request, username):
    user = get_object_or_404(User, username=username)
    me = request.user
    if not me.is_authenticated:
        return redirect("signup")
    checking_date_requests = Dates.objects.filter(receiver=user, sender=me)
    if not DateRequests.objects.filter(user=user).exists():
        DateRequests.objects.create(user=user, requests = 0 )
    get_no_of_requests = DateRequests.objects.get(user=user)
    no_of_requests = get_no_of_requests.requests
    get_username = user.username
    details = Details.objects.get(user=user)
    fullname = f"{details.fname} {details.lname}"
    return render(
        request,
        "home/profile.html",
        {
            "details": details,
            "fullname": fullname,
            "user": user,
            "username": get_username,
            "check": checking_date_requests,
            "no_of_requests": no_of_requests,
        },
    )


def Search(request):
    users = None
    query = None
    meuser = request.user
    if not meuser.is_authenticated:
        return redirect("signup")
    if not Details.objects.filter(user=meuser).exists() :
        return redirect("details")
    if request.method == "POST":
        query = request.POST["search"]
        if query:
            users = User.objects.filter(username__icontains=query)
            for user in users:
                details = Details.objects.filter(
                    user=user
                ).first()  # Safely retrieve details
                user.bio = (
                    details.bio if details else "No bio available"
                )  # Attach bio to user object
                if details and details.images:
                    user.images = details.images.url  # Use the URL of the image
                else:
                    user.images = "/static/default.png"
        else:
            users = User.objects.none()
    return render(request, "home/search.html", {"users": users, "query": query})


def date_requests(request, username):
    user = request.user
    if not user.is_authenticated:
        return redirect("signup")
    reciever = User.objects.get(username=username)
    if not Details.objects.filter(user=user).exists() :
        return redirect("details")
    link_requests = Dates.objects.create(receiver=reciever, sender=user)
    dates = DateRequests.objects.filter(user=reciever).first()

    if DateRequests.objects.filter(user=reciever).exists():
        total_requests = dates.requests
        DateRequests.objects.filter(user=reciever).update(requests=total_requests + 1)
        messages.success(request, "date request sent successfully")
    else:
        DateRequests.objects.create(user=reciever)
        messages.success(request, "date request sent successfully")
    return redirect(SomeUser, reciever)

def followers(request, username):
    followers = None
    followers_of = username
    username_for_follwerlist = User.objects.get(username = username)
    followers = Dates.objects.filter(receiver = username_for_follwerlist)
    
    for follower in followers:
        usernames = follower.sender
        follower.username = usernames.username
        details = Details.objects.filter(
                    user=usernames
                ).first()
        
        if details and details.images:
            follower.images = details.images.url 
        else:
            follower.images = "/static/default.png"
        if details and details.bio:
            follower.bio = details.bio
        else:
            follower.bio = "No bio Available"
        
    return render(request, "home/followers.html", {"followers": followers, "followers_of": followers_of})