from django.db.models import Count
from products.models import Category


class DataMixin:
    # Пагинация:
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count("product"))

        context["categories"] = categories
        if "category_selected" not in context:
            context["category_selected"] = 0

        return context
