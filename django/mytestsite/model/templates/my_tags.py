from atexit import register
from django import template
from django.utils.safestring import mark_safe
register=template.Library()
@register.filter
def image(v1):
  f=v1.replace(' ','_')
  return 'images/'+f+'.png'