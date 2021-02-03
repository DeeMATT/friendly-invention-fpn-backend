from django.shortcuts import render
from django.conf import settings
from api_utils.views import (
    badRequestResponse, InternalServerError, successResponse, createdResponse,
    unAuthenticatedResponse, unAuthorizedResponse, resourceConflictResponse, 
    resourceNotFoundResponse, paginatedResponse, getUserIpAddress
)


def provisionUser(request):
    # check for root secret in header
    secret = request.headers.get('Secret')
    if not secret == settings.SECRET:
        return unAuthorizedResponse(errorCode=ErrorCodes.INVALID_CREDENTIALS, message=getInvalidCredentialsErrorPacket())

    ## decode the request body
    body = json.loads(request.body)

    # check if required fields are present in request payload
    missingKeys = validateKeys(payload=body, requiredKeys=['email', 'firstName', 'lastName', 'userName', 'password', 'phone'])
    if missingKeys:
        return badRequestResponse(ErrorCodes.MISSING_FIELDS, message=f"The following key(s) are missing in the request payload: {missingKeys}")

    # validate if the email is in the correct format
    if not validateEmailFormat(body['email']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS, message = "Email format is invalid")
    
    if not validateThatStringIsEmptyAndClean(body['firstName']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS, message = "First name can not contain special characters")
    
    if not validateThatStringIsEmptyAndClean(value=body['lastName']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS, message = "Last name can not contain special characters")
    
    if not validateThatAStringIsClean(body['userName']):
        return badRequestResponse(errorCode = ErrorCodes.GENERIC_INVALID_PARAMETERS, message = "User name can not contain special characters")

    # check if user with that email exists
    if getUserByEmail(body['email'], ) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST, 
                                message = getUserAlreadyExistErrorPacket(value='email'))

    # check if user with that username exists
    if getUserByUserName(body['userName'], ) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST, 
                                message = getUserAlreadyExistErrorPacket(value='username'))

    ## check if user with that phone exists
    if getUserByPhone(body['phone'], ) is not None:
        return resourceConflictResponse(errorCode=ErrorCodes.USER_ALREADY_EXIST, 
                                message = getUserAlreadyExistErrorPacket(value='phone'))

    # create userProfile
    user = createUserRecord(firstName=body['firstName'], lastName=body['lastName'], userName=body['userName'], 
                            email=body['email'], phone=body['phone'], password=body['password'])
    
    if user is not None:
        return successResponse(message="successfully created", body=transformUser(user))
