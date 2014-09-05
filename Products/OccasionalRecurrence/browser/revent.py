# encoding: utf-8
"""
Helper view for individual recurring events
"""

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

import caldate

range_functions = {
    u'daily': caldate.daily,
    u'weekly': caldate.weekly,
    u'biweekly': caldate.biweekly,
    u'monthly': caldate.monthly,
}

class REvent(BrowserView):

    def __init__(self, context, request):
        super(REvent, self).__init__(context, request)
        self.localize = getToolByName(context, 'translation_service').toLocalizedTime

    def clean_time(self, atime):
        return self.localize(atime, time_only=True).strip('0').replace(' ', '').lower()

    def clean_date(self, adate):
        return self.localize(adate).replace(' 0', ' ')

    def getScheduleStrings(self):
        """
        Returns a list of strings to describe an event's scheduling.
        Typically, the strings will be displayed sequentially with
        some break between strings.

        Number of string is flexible.
        """

        context = self.context

        start = context.start()
        end = context.end()
        recurs = getattr(context, 'recurs', 'daily')
        today = DateTime()

        erange = range_functions[recurs](start, end, today)
        dstart = erange[0]
        dend = erange[-1]
        same_day = dstart == dend
        long_term = (dend - dstart) > 365
        start_time = self.clean_time(start)
        end_time = self.clean_time(end)
        same_time = start_time == end_time
        all_day = same_time and (start_time == '12:00am')

        rez = [self.clean_date(start)]
        if not all_day:
            if same_time:
                rez.append(start_time)
            else:
                rez.append('%s - %s' % (start_time, end_time))
        if not same_day:
            if long_term:
                rez.append(recurs)
            else:
                rez.append('%s until', recurs)
                rez.append(self.clean_date(end))

        return rez
