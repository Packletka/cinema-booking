from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Получить значение из словаря по ключу в шаблоне
    Использование: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return []
    return dictionary.get(key, [])
