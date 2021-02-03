import re
from data_transformer.views import stringIsInteger


def validateEmailFormat(email):
    emailPattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

    if(re.search(emailPattern, email)):
        return True

    return False


def validatePhoneFormat(phone):
    if not stringIsInteger(phone):
        return False

    # valid phone format for Nigeria without international dialing code e.g 081********
    if phone.startswith('+'):
        return len(phone) == 14
    elif phone.startswith('234'):
        return len(phone) == 13
    else:
        return len(phone) == 11


def validateThatAStringIsClean(value):
    regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
    return (regex.search(value) == None)


def validateThatStringIsEmpty(value):
    return (len(value.strip()) > 0)


def validateThatStringIsEmptyAndClean(value):
    is_clean = (re.compile(r'[@_!#$%^&*()<>?/\|}{~:]').search(value) == None)
    not_empty = (len(value.strip()) != 0)

    return (is_clean and not_empty)


def validateThatListIsEmpty(value):
    return (len(value) > 0)


def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys
