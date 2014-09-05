#!/usr/bin/env python
# encoding: utf-8
"""
interfaces.py

"""

from zope.interface import Interface
from zope.interface import Attribute


class IRCalendarView(Interface):
    """
        A browser view providing functionality that is a superset to
        the calendar tool with the addition of recurrence.
    """

    def DateTime():
        """ """

    def current():
        """ """

    def current_day():
        """ """

    def nextYearMax():
        """ """

    def prevYearMin():
        """ """

    def year():
        """ """

    def month():
        """ """

    def prevMonthTime():
        """ """

    def nextMonthTime():
        """ """

    def weeks():
        """ """

    def showStates():
        """ """

    def showPrevMonth():
        """ """

    def showNextMonth():
        """ """

    def getYearAndMonthToDisplay():
        """ """

    def getPreviousMonth(month, year):
        """ """

    def getNextMonth(month, year):
        """ """

    def getWeekdays(self):
        """Returns a list of Messages for the weekday names."""

    def getEnglishMonthName(self, month):
        """Returns the English month name."""

    def getMonthName(self, month):
        """Returns the month name as a Message."""

    def isToday(self, day):
        """Returns True if the given day and the current month and year equals
           today, otherwise False.
        """

    def getevents(context, first, last):
        """ given start and end dates, return a list of days that have events
        """

    def getDayNumbers(self):
        """ wrapper for calendar tool equivalent """

    def getNextDaysEvents(context, days):
        """
          return the next days worth of events
        """

    def getNextMonthEvents(context):
        """
          returns next month worth of events
        """

    def getNextWeekEvents(context):
        """
          returns next week worth of events
        """

    def getTodayEvents(context):
        """
          returns today's events
        """

    def getQueryString(self):
        """ return query string """