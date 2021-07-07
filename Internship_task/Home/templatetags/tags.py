from django import template
register = template.Library()

@register.filter
def Average(grade_list):

    return round((sum([int(i) for i in grade_list])/5),2)

@register.filter
def Convert(string):
    convert = int(string)
    if (convert >= 130) :  return "Very Superior"
    elif (convert >= 120 ) :  return "Superior"
    elif (convert >= 110 ) :  return "Above average"
    elif (convert >= 85 ) :  return "Average"
    elif (convert >= 70 ) :  return "Borderline"
    elif (convert >= 50 ) :  return "Mild Intellectual Disability"
    elif (convert >= 35 ) :  return "Moderate"
    elif (convert >= 20 ) :  return "Severe"
    return "Profound"
