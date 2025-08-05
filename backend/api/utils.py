from django.utils.text import slugify
import uuid

def generate_unique_slug(instance, name, model_class, slug_field='slug'):
    base_slug = slugify(name)
    slug = base_slug
    num = 1

    while model_class.objects.filter(**{slug_field: slug}).exists():
        # You can choose to append a number or short UUID instead of `num`
        slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"  # shorter random value

    return slug
