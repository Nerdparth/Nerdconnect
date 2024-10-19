from django.contrib import admin
from django.urls import path
from authentication.views import (
    signup,
    logout_view,
    login_view,
    detail_section,
    UpdateDetails,
    DeleteAccount,
    index,
)
from home.views import (
    home,
    CreatePost,
    feedSection,
    SomeUser,
    Search,
    UserPosts,
    date_requests,
    followers,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", signup, name="signup"),
    path("user/<str:username>", home, name="home"),
    path("create/", CreatePost, name="create"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("details/", detail_section, name="details"),
    path("updatedetails/", UpdateDetails, name="updatedetails"),
    path("user/delete/", DeleteAccount, name="delete"),
    path("feed/", feedSection, name="feed"),
    path("profile/<str:username>", SomeUser, name="someuser"),
    path("search/", Search, name="search"),
    path("posts/", UserPosts, name="userposts"),
    path("send_request/<str:username>", date_requests, name="daterequest"),
    path("followers/<str:username>", followers, name="followers"),
    path("", index)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
