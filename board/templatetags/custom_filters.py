from django import template
from board.models import Author

register = template.Library()


# проверяет, является ли User автором
@register.filter()
def user_is_author(user):
   set = Author.objects.filter(author=user)
   if set:
      return set[0].is_subscriber
   else:
      return False