from .models import Category

def categories(request):
    """
    Context processor to make all categories available in all templates
    """
    return {
        'categories': Category.objects.all().order_by('name')
    }

