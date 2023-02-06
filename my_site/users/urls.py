from django.urls import path
from users.views import (EmailVerificationView, LogoutUser, ProfileUser,
                         UserRegistrationAjaxView, loginAjaxView)

urlpatterns = [
    path('login_ajax/', loginAjaxView.as_view(), name="login_ajax"),
    path('registration_ajax/', UserRegistrationAjaxView.as_view(), name="registration_ajax"),
    path('logout/', LogoutUser, name="logout"),
    path('profile/', ProfileUser, name="profile"),
    path('verify/<str:email>/<uuid:email_code>', EmailVerificationView.as_view(), name="email_verification"),

]
