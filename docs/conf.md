# Twitter Dev keys:

## Terminology:
**API Key and Secret**: Essentially the username and password for your App. You will use these to authenticate requests that require OAuth 1.0a User Context, or to generate other tokens such as user Access Tokens or App Access Token.

**Access Token and Secret**: In general, Access Tokens represent the user that you are making the request on behalf of. The ones that you can generate via the developer portal represent the user that owns the App. You will use these to authenticate requests that require OAuth 1.0a User Context. If you would like to make requests on behalf of another user, you will need to use the 3-legged OAuth flow for them to authorize you. 

**Client ID and Client Secret**: These credentials are used to obtain a user Access Token with OAuth 2.0 authentication. Similar to OAuth 1.0a, the user Access Tokens are used to authenticate requests that provide private user account information or perform actions on behalf of another account but, with fine-grained scope for greater control over what access the client application has on the user. 

**App only Access Token**: You will use this token when making requests to endpoints that responds with information publicly available on Twitter.
