
Employees endpoints.

Authenticate
============

**/api/employee/authenticate/**

* Using curl:

```bash
curl -X POST -d "username=sinfante&password=allstars" https://bxconnect.herokuapp.com:443/api/employee/authenticate/
```

* Using postman:


![Authentication using POSTMAN](http://i.imgur.com/TP009D3.png 'Authentication using POSTMAN')

* Using httpie:

```bash
http -f POST https://bxconnect.herokuapp.com:443/api/employee/authenticate/ username='sinfante' password='allstars'
```

#### Authenticate Response

```bash
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Connection: keep-alive
Content-Type: application/json
Date: Tue, 13 Dec 2016 13:52:56 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "is_base_profile_complete": false,
    "is_password_reset_required": true,
    "is_staff": true,
    "reset_password_code": null,
    "token": "0c82ba3493b9369e800fff58687c06220fa34d77",
    "user_id": 1
}
```

Create
======

**/api/employee/create/**

* Using curl:

```bash
curl -X POST -d "email=sinfante@belatrixsf.com" https://bxconnect.herokuapp.com:443/api/employee/create/
```

* Using postman:


![Create using POSTMAN](http://i.imgur.com/yWd8Pwz.png 'Create using POSTMAN')

* Using httpie:

```bash
http -f POST https://bxconnect.herokuapp.com:443/api/employee/create/ email='sinfante@belatrixsf.com'
```

#### Create Response

```bash
HTTP/1.1 201 Created
Allow: POST, OPTIONS
Connection: keep-alive
Content-Type: application/json
Date: Tue, 13 Dec 2016 14:21:40 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "detail": "User(s) successfully created."
}
```
