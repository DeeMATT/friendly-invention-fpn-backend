from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil import tz, parser
import pytz


def stringIsNumber(value):
    try:
        return (stringIsInteger(value) or stringIsFloat(value))
    except:
        return False


def stringIsInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def stringIsFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def stringIsBoolean(value):
    try:
        bool(value)
        return True
    except ValueError:
        return False


def stringIsDate(value):
    try:
        return not convertStringToDate(value) is None
        # return (dateIsNotISO(value) or dateIsISO(value))
    except:
        return False


def dateIsNotISO(value):
    try:
        if value != datetime.strptime(value, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


def toUiReadableDateFormat(value):
    try:
        if value is None:
            return ""

        localizedValue = timezone.localtime(
            value, pytz.timezone('Africa/lagos'))
        return datetime.strftime(localizedValue, "%b %d, %Y %I:%M%p")
    except Exception as ex:
        print(ex)
        return str(value)


def toUiReadableDateOnlyFormat(value):
    try:
        localizedValue = timezone.localtime(
            value, pytz.timezone('Africa/lagos'))
        return datetime.strftime(localizedValue, "%Y-%m-%d")
    except Exception as ex:
        print("exception was thrown ", ex)
        return ""


def dateTimeIsISO(value):
    try:
        # can validate 2019-03-04T20:18:12Z
        if value != datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ"):
            raise ValueError
        return True
    except ValueError:
        return False


def dateIsISO(value):
    try:
        # can validate 2019-03-04
        if value != str(datetime.strptime(value, "%Y-%m-%d").date()):
            raise ValueError
        return True
    except ValueError:
        return False


def convertStringToDate(value, dayFirst=True):
    try:
        return parser.parse(value, dayfirst=dayFirst)
    except ValueError:
        return None


def convertStringToDateTz(value, dayFirst=True):
    try:

        dateValue = parser.parse(value, dayfirst=dayFirst)

        pst = pytz.timezone('Africa/Lagos')
        d = pst.localize(dateValue)

        return d
    except ValueError:
        return None


def timezoneAwareDate(date, tzinfo='Africa/Lagos'):
    try:
        realTzInfo = pytz.timezone(tzinfo)
        return date.astimezone(realTzInfo)
    except ValueError:
        return None

