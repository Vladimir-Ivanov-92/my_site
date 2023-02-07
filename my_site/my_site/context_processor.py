from baskets.models import BasketAuth, BasketFK
from users.forms import UserLoginForm, UserRegistrationForm

menu = [
    {
        "title": "Каталог",
        "url_name": "products_catalog"
    },
    {
        "title": "Доставка и оплата",
        "url_name": "delivery_and_pay_page"
    },
]

contacts = {"title": "Контакты"}

contacts_dropdown = [
    {
        "title": "О нас",
        "url_name": "....."
    },
    {
        "title": "Адреса и телефоны",
        "url_name": "..."
    },
    {
        "title": "Обратная связь",
        "url_name": "feedback_page"
    },
]

menu_user = {
    "title": "Меню",
    "logout": "Выйти",
    "url_logout": "logout"

}

menu_user_dropdown = [
    {
        "title": "Профиль",
        "url_name": "profile"
    },
    {
        "title": "Заказы",
        "url_name": "orders_list"
    },
    # {
    #     "title": "Админ панель",
    #     "url_name": "admin:index"  # FIXMI заменить ссылкой на админку!
    # },

]


def get_context_data(request):
    user = request.user
    if user.is_authenticated:
        baskets = BasketAuth.objects.filter(user=request.user)
        baskets_product_id = BasketAuth.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        try:
            baskets = BasketFK.objects.filter(csrftoken=request.COOKIES['csrftoken'])
            baskets_product_id = BasketFK.objects.filter(csrftoken=request.COOKIES['csrftoken']).values_list(
                'product_id', flat=True)
        except KeyError:
            baskets = None
            baskets_product_id = None

    update_menu = menu.copy()
    update_contacts_dropdown = contacts_dropdown.copy()
    update_menu_user_dropdown = menu_user_dropdown.copy()

    context = {
        "form_login": UserLoginForm(),
        "form_registration": UserRegistrationForm(),
        "baskets": baskets,
        "menu": update_menu,
        "contacts": contacts,
        "contacts_dropdown": update_contacts_dropdown,
        "menu_user": menu_user,
        "menu_user_dropdown": update_menu_user_dropdown,
        "baskets_product_id": baskets_product_id,
        "view_cards": True,
    }

    return context
