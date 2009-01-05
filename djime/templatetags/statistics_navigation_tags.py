from django import template
import datetime

register = template.Library()

def do_statistics_nav_vars(parser, token):
    if len(token.contents.split()) != 2:
        raise template.TemplateSyntaxError, "%r tag needs a single argument" % token.contents.split()[0]
    if token.contents.split()[1] not in ['get']:
        raise template.TemplateSyntaxError, "%r tag valid arguments is: get" % token.contents.split()[0]
    now = datetime.datetime.now()
    current_week = now.isocalendar()[1]
    current_week_year = now.isocalendar()[0]
    current_month = now.month
    current_month_year = now.year
    last_week_date = now - datetime.timedelta(days=7)
    last_week = last_week_date.isocalendar()[1]
    last_week_year = last_week_date.isocalendar()[0]
    if current_month != 1:
        last_month = current_month - 1
        last_month_year = current_month_year
    elif current_month == 1:
        last_month = 12
        last_month_year = current_month_year - 1
    action = token.contents.split()[1]
    return StatisticsNavVarsNode(current_week, current_week_year, current_month, current_month_year, last_week, last_week_year, last_month, last_month_year, action)


class StatisticsNavVarsNode(template.Node):
    def __init__(self, current_week, current_week_year, current_month, current_month_year, last_week, last_week_year, last_month, last_month_year, action):
        self.current_week = current_week
        self.current_week_year = current_week_year
        self.current_month = current_month
        self.current_month_year = current_month_year
        self.last_week = last_week
        self.last_week_year = last_week_year
        self.last_month = last_month
        self.last_month_year = last_month_year
        self.action = action
    def render(self, context):
        if self.action == 'get':    
            context['statistics_nav_current_week'] = self.current_week
            context['statistics_nav_current_week_year'] = self.current_week_year
            context['statistics_nav_current_month'] = self.current_month
            context['statistics_nav_current_month_year'] = self.current_month_year
            context['statistics_nav_last_week'] = self.last_week
            context['statistics_nav_last_week_year'] = self.last_week_year
            context['statistics_nav_last_month'] = self.last_month
            context['statistics_nav_last_month_year'] = self.last_month_year
            return ''


register.tag('statistics_nav_vars', do_statistics_nav_vars)