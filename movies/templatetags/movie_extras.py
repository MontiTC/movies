from django import template

register = template.Library()

@register.filter
def duration_to_hms(minutes):
    if not minutes:
        return ""
    hours, minutes = divmod(minutes, 60)
    return f"{hours} hrs {minutes} mins"
