# Sanic-JWT-Login
Sanic extension that helps authentication using JWT(Json Web Token), token will refresh after 15 minutes

## Guide
- to get jwt token, go to route `..../jwt` 
- each time when user login, or signup, ... must provide a jwt token in headers
```
-H "Authorization: Bearer <token>"
```
- username and password is stored in mongodb
- api will look up information in db to check if account is valid