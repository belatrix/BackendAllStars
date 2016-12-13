
Employees endpoints.


Authenticate
============

**Note:** This endpoint gives authorization token, token is needed to use other endpoints.

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

Create Bulk
===========

**/api/employee/create/bulk/**

* Using curl:

```bash
curl -X POST -d '{"password":"12345","emails":[{"email":"newuser1@belatrixsf.com"},{"email":"newuser2@belatrixsf.com"}]}' -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453' -H 'Content-Type: application/json' https://bxconnect.herokuapp.com:443/api/employee/create/bulk/
```

* Using postman:

![Create Bulk using POSTMAN 1](http://i.imgur.com/BsZviaV.png 'Create Bulk using POSTMAN 1')
![Create Bulk using POSTMAN 2](http://i.imgur.com/i0fZmiM.png 'Create Bulk using POSTMAN 2')

* Using httpie:

```bash
http POST https://bxconnect.herokuapp.com:443/api/employee/create/bulk/ 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453' <<< '{"password":"12345","emails":[{"email":"newuser1@belatrixsf.com"},{"email":"newuser2@belatrixsf.com"}]}'
```

#### Create Bulk Response

```bash
HTTP/1.0 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Date: Tue, 13 Dec 2016 15:38:30 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Cookie
X-Frame-Options: SAMEORIGIN

{
    "detail": "User(s) successfully created."
}
```

List
====

**/api/employee/list/**

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/list/ -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or
```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/list.json -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or if you want to perform a search
```bash
curl -X GET 'https://bxconnect.herokuapp.com:443/api/employee/list.json?search=ser' -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```


* Using postman:

![Employee list using POSTMAN](http://i.imgur.com/kbbrtuF.png 'Employee list using POSTMAN')

* Using httpie:

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list/ 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or
```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list.json 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or if you want to perform a search
```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list.json search==ser 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```

#### List response
```bash
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Connection: keep-alive
Content-Type: application/json
Date: Tue, 13 Dec 2016 19:13:03 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "avatar": null,
            "current_month_score": 40,
            "current_year_score": 40,
            "email": "sinfante@belatrixsf.com",
            "first_name": "Sergio",
            "is_blocked": false,
            "last_month_score": 0,
            "last_name": "Infante Montero",
            "last_year_score": 0,
            "level": 1,
            "location": {
                "icon": "https://i.imgur.com/CpYIGjr.png",
                "id": 1,
                "name": "Lima"
            },
            "pk": 1,
            "total_score": 40,
            "username": "sinfante"
        }
    ]
}
```

List deactivated
================

**/api/employee/list/deactivated/**

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/list/deactivated/ -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or
```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/list/deactivated.json -H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```

* Using postman:

![Employee list deactivated using POSTMAN](http://i.imgur.com/ivnMps7.png 'Employee list deactivated using POSTMAN')

* Using httpie:

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list/deactivated/ 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```
or
```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list/deactivated.json 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```

#### List response
```bash
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Connection: keep-alive
Content-Type: application/json
Date: Tue, 13 Dec 2016 19:34:38 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "avatar": null,
            "current_month_score": 0,
            "current_year_score": 0,
            "email": "dsanchez@belatrixsf.com",
            "first_name": "Daniel",
            "is_blocked": true,
            "last_month_score": 0,
            "last_name": "Sanchez",
            "last_year_score": 0,
            "level": 0,
            "location": {
                "icon": "https://i.imgur.com/CpYIGjr.png",
                "id": 1,
                "name": "Lima"
            },
            "pk": 17,
            "total_score": 0,
            "username": "dsanchez"
        }
    ]
}
```