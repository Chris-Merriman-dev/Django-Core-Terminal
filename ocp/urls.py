from django.urls import path

from . import views

urlpatterns = [
    #basic guest urls
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("mission", views.mission, name="mission"),
    path("currentproducts", views.currentproducts, name="currentproducts"),
    path("comingsoon", views.comingsoon, name="comingsoon"),
    path("employment", views.employment, name="employment"),

    #ability to login, logout and register users
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #dashboard that loads when you login
    path("dashboard", views.dashboard, name="dashboard"),

    #handles the chat with ollama (ED-209)
    path("chat", views.chat, name="chat"),
    path("chat_ed209", views.chat_ed209, name="chat_ed209"),
    path("get_chat_history", views.get_chat_history, name="get_chat_history"),

    #handles image creation with COMFYUI
    path("image_creation/", views.image_creation, name="image_creation"),
    path('health_check/', views.health_check, name='health_check'),
    path("generate_vision/", views.generate_vision, name="generate_vision"),

    #will display the assets (images created) and commenting on images
    path("assetfeed/", views.assetfeed, name="assetfeed"),
    path('asset/<int:asset_id>/comment/', views.add_comment, name='add_comment'),

    #loads the user profile
    path("user_profile/<int:user_id>/", views.user_profile, name="user_profile"),

    #loads the security settings page for updating users access levels
    path("security_settings", views.security_settings, name="security_settings"),

    #allows update of the user access level
    path("update_access/<int:user_id>/", views.update_access, name="update_access"),

 
]