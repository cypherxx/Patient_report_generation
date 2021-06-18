from django import template
register = template.Library()

@register.filter
def Average(grade_list):

    return round((sum([int(i) for i in grade_list])/5),2)

@register.filter
def Convert(string):
    convert = int(string)
    return ('borderline' if convert < 90 else 'average')
