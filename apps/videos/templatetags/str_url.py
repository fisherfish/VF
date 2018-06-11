from django import template

register=template.Library() #对象名必须为register
@register.filter
def str_imagefield(url):
    return str(url)[:4]