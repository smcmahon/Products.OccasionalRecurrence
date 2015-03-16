#!/usr/bin/env python
# encoding: utf-8
"""
caldate.py

Copyright (c) 2009 Stephen McMahon. Licensed under the GPL.

DocTests for caldate

    >>> start = DateTime('2009/04/01 00:00:00 GMT-7')

    >>> end = DateTime('2009/04/30 00:00:00 GMT-7')

    >>> daily(start, start, start)
    [DateTime('2009/04/01 00:00:00 GMT-7')]

    >>> daily(start, end, end)
    [DateTime('2009/04/30 00:00:00 GMT-7')]

    >>> len(daily(start, end, start))
    30

    >>> len(daily(start, end, DateTime('2009/04/16 00:00:00 GMT-7')))
    15

    >>> target = DateTime('2009/04/10 00:00:00 GMT-7')
    >>> weekly(start, end, target)
    [DateTime('2009/04/10 00:00:00 GMT-7'), DateTime('2009/04/17 00:00:00 GMT-7'), DateTime('2009/04/24 00:00:00 GMT-7')]

    >>> target = DateTime('2009/03/10 00:00:00 GMT-7')
    >>> weekly(start, end, target)
    [DateTime('2009/04/07 00:00:00 GMT-7'), DateTime('2009/04/14 00:00:00 GMT-7'), DateTime('2009/04/21 00:00:00 GMT-7'), DateTime('2009/04/28 00:00:00 GMT-7')]

    >>> target = DateTime('2009/04/01 00:00:00 GMT-7')
    >>> weekly(start, end, target)
    [DateTime('2009/04/01 00:00:00 GMT-7'), DateTime('2009/04/08 00:00:00 GMT-7'), DateTime('2009/04/15 00:00:00 GMT-7'), DateTime('2009/04/22 00:00:00 GMT-7'), DateTime('2009/04/29 00:00:00 GMT-7')]

    >>> target = DateTime('2009/04/30 00:00:00 GMT-7')
    >>> weekly(start, end, target)
    [DateTime('2009/04/30 00:00:00 GMT-7')]

    >>> weekly(start, end, start-1)
    [DateTime('2009/04/07 00:00:00 GMT-7'), DateTime('2009/04/14 00:00:00 GMT-7'), DateTime('2009/04/21 00:00:00 GMT-7'), DateTime('2009/04/28 00:00:00 GMT-7')]

    >>> weekly(start, end, start+1)
    [DateTime('2009/04/02 00:00:00 GMT-7'), DateTime('2009/04/09 00:00:00 GMT-7'), DateTime('2009/04/16 00:00:00 GMT-7'), DateTime('2009/04/23 00:00:00 GMT-7'), DateTime('2009/04/30 00:00:00 GMT-7')]

    >>> [d.dow() for d in weekly(DateTime('2012/06/20 21:45'), DateTime('2012/07/31'), DateTime('2012/06/20 21:45'))]
    [3, 3, 3, 3, 3, 3]

    >>> target = DateTime('2009/05/01 00:00:00 GMT-7')
    >>> weekly(start, end, target)
    []

    >>> weekly(target, target, target)
    [DateTime('2009/05/01 00:00:00 GMT-7')]

    >>> start = DateTime('2009/05/01 00:00:00 GMT-7')
    >>> end = DateTime('2009/05/31 00:00:00 GMT-7')

    >>> target = DateTime('2009/05/01 00:00:00 GMT-7')
    >>> biweekly(start, end, target)
    [DateTime('2009/05/01 00:00:00 GMT-7'), DateTime('2009/05/15 00:00:00 GMT-7'), DateTime('2009/05/29 00:00:00 GMT-7')]

    >>> target = DateTime('2009/04/30 00:00:00 GMT-7')
    >>> biweekly(start, end, target)
    [DateTime('2009/05/14 00:00:00 GMT-7'), DateTime('2009/05/28 00:00:00 GMT-7')]

    >>> target = DateTime('2009/05/02 00:00:00 GMT-7')
    >>> biweekly(start, end, target)
    [DateTime('2009/05/02 00:00:00 GMT-7'), DateTime('2009/05/16 00:00:00 GMT-7'), DateTime('2009/05/30 00:00:00 GMT-7')]

    >>> target = DateTime('2009/06/01 00:00:00 GMT-7')
    >>> biweekly(start, end, target)
    []

    >>> monthly(start, end, DateTime('2009/04/01 00:00:00 GMT-7'))
    [DateTime('2009/05/06 00:00:00 GMT-7')]

    >>> DateTime('2009/04/01 00:00:00 GMT-7').dow() == monthly(start, end, DateTime('2009/04/01 00:00:00 GMT-7'))[0].dow()
    True

    >>> monthly(start, end, DateTime('2009/04/15 00:00:00 GMT-7'))
    [DateTime('2009/05/20 00:00:00 GMT-7')]

    >>> DateTime('2009/04/15 00:00:00 GMT-7').dow() == monthly(start, end, DateTime('2009/05/20 00:00:00 GMT-7'))[0].dow()
    True

    >>> monthly(start, end, DateTime('2009/04/30 00:00:00 GMT-7'))
    []

    >>> monthly(start, DateTime('2009/06/30 00:00:00 GMT-7'), DateTime('2009/04/30 00:00:00 GMT-7'))
    []

    >>> monthly(start, DateTime('2009/07/31 00:00:00 GMT-7'), DateTime('2009/04/30 00:00:00 GMT-7'))
    [DateTime('2009/07/30 00:00:00 GMT-7')]

    >>> monthly(start, DateTime('2009/07/31 00:00:00 GMT-7'), DateTime('2009/05/12 16:32 GMT-7'))
    [DateTime('2009/05/12 00:00:00 GMT-7'), DateTime('2009/06/09 00:00:00 GMT-7'), DateTime('2009/07/14 00:00:00 GMT-7')]

"""

import calendar
from DateTime import DateTime


def stripTime(target):
    return DateTime(target.Date())
    parts = target.parts()
    return DateTime(parts[0], parts[1], parts[2])


def hardRecurr(start, end, target, offset):
    """
      For fixed-day count recurrance
    """

    start = stripTime(start)
    target = stripTime(target)
    res = []
    if target.lessThanEqualTo(end):
        if start.lessThan(target):
            start = target
        day = start + (int(round(target - start)) + offset) % offset
        while day.lessThanEqualTo(end):
            res.append(day)
            day += offset
    return res


def daily(start, end, target):
    adate = max(start, target)
    res = []
    while adate <= end:
        res.append(adate)
        adate += 1
    return res


def weekly(start, end, target):
    """
      Find the day of week for target,
      return dates for all the same weekdays
      inclusively between start and end.

    """
    return hardRecurr(start, end, target, 7)


def biweekly(start, end, target):
    """
      Alternate weeks
    """

    return hardRecurr(start, end, target, 14)


def startOfMonth(adate):
    return adate - (adate.day() - 1)


def startOfNextMonth(adate):
    return endOfMonth(adate) + 1


def endOfMonth(adate):
    days_in_month = calendar.monthrange(adate.year(), adate.month())[1]
    parts = adate.parts()
    return DateTime(parts[0], parts[1], days_in_month)


def monthly(start, end, target):
    """
      Follow an xth weekday in month pattern
    """

    week = target.day() / 7
    tdow = target.dow()

    if target > start:
        monthStart = startOfMonth(stripTime(target))
    else:
        monthStart = startOfMonth(start)

    # import pdb; pdb.set_trace()

    res = []
    while monthStart <= end:
        msdow = monthStart.dow()
        if tdow >= msdow:
            ofs = tdow - msdow
        else:
            ofs = 7 - (msdow - tdow)
        date = monthStart + (week * 7 + ofs)
        # if monthStart <= date <= endOfMonth(monthStart):
        if start <= date <= endOfMonth(monthStart):
            res.append(date)
        monthStart = startOfNextMonth(monthStart)
    return res


if __name__ == "__main__":
    import doctest
    doctest.testmod()
