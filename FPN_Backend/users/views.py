from django.shortcuts import render
from django.conf import settings
from errors.views import getError, ErrorCodes
from api_utility.views import (
    badRequestResponse, internalServerError, successResponse, createdResponse,
    unAuthenticatedResponse, unAuthorizedResponse, resourceConflictResponse, 
    resourceNotFoundResponse, paginatedResponse, getUserIpAddress
)
from api_utility.validators import (
    validateKeys, validateEmailFormat, validatePhoneFormat, 
    validateThatStringIsEmptyAndClean, validateThatStringIsEmpty
)
from .utils import (
    getUserByEmail, getUserById, getUserByPhone, getUserByUsername, createUser
)
from data_transformer.serializers import transformUser
import json
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def provisionUser(request):
    # check for root secret in header
    secret = request.headers.get('Secret')
    if not secret == settings.SECRET:
        return unAuthorizedResponse(getError(ErrorCodes.UNAUTHORIZED_REQUEST, "Invalid Secret Key"))

    ## decode the request body
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['email', 'firstName', 'lastName', 'username', 'password', 'phone'])
    if missingKeys:
        return badRequestResponse(getError(ErrorCodes.MISSING_FIELDS, f"The following key(s) are missing in the request payload: {missingKeys}"))

    # validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(getError(ErrorCodes.GENERIC_ERROR, message="Email format is invalid")
    
    if not validateThatStringIsEmptyAndClean(body['firstName']):
        return badRequestResponse(getError(ErrorCodes.GENERIC_ERROR, message="First name can not contain special characters")
    
    if not validateThatStringIsEmptyAndClean(value=body['lastName']):
        return badRequestResponse(getError(ErrorCodes.GENERIC_ERROR, message="Last name can not contain special characters")

    # check if user with that email exists
    if getUserByEmail(body['email']):
        return resourceConflictResponse(getError(ErrorCodes.USER_ALREADY_EXISTS, message="A user already exists with same email"))

    # check if user with that username exists
    if getUserByUsername(body['username']) is not None:
        return resourceConflictResponse(getError(ErrorCodes.USER_ALREADY_EXISTS, message="A user already exists with same username"))

    ## check if user with that phone exists
    if getUserByPhone(body['phone']) is not None:
        return resourceConflictResponse(getError(ErrorCodes.USER_ALREADY_EXISTS, message="A user already exists with same phone"))

    # create userProfile
    user = createUser(
                firstName=body['firstName'], 
                lastName=body['lastName'], 
                username=body['userName'], 
                email=body['email'], 
                phone=body['phone'], 
                password=body['password']
            )
    
    if user:
        return createdResponse(message="successfully created", body=transformUser(user))
