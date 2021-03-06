
Employees endpoints.


Authenticate
============

**Note:** This endpoint gives authorization token, token is needed to use other endpoints, this token doesn't have expiring time.

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


**/api/employee/token-auth/**

**Note:** This endpoint gives authorization JSON Web Token, token is needed to use other endpoints, this token has expiring time (30 min).

* Using curl, response should be similar to previous above:

```bash
curl -X POST -d "username=sinfante&password=allstars" https://bxconnect.herokuapp.com:443/api/employee/token-auth/
```

To use this JWT Token with other endpoints you should replace:

```
-H 'Authorization: Token 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```

with this

```
-H 'Authorization: JWT 949663fa5ac153d6fb57ac95251380a2ad8e3453'
```

**/api/employee/token-refresh/**

**Note:** This endpoint gives authorization JSON Web Token, token is needed to use other endpoints, this token has expiring time (30 min).

* Using curl, response should be similar to previous above:

```bash
curl -X POST -d "token=eyJ0eXAiOiJKV1QiLCJhbGciOi" https://bxconnect.herokuapp.com:443/api/employee/token-refresh/
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

Top List
========

**/api/employee/list/top/{kind}/{quantity}/**

| **{kind}**          |
|---------------------|
| total_score         |
| level               |
| current_month_score |
| current_year_score  |
| last_month_score    |
| last_year_score     |

**{quantity}**:  # of result elements

* Using curl (example top 3 of total_score):

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/list/top/total_score/3/ -H 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

* Using postman:

![Employee top list using POSTMAN](http://i.imgur.com/LZhFplq.png 'Employee top list using POSTMAN')

* Using httpie (example top 3 of total_score):

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/list/top/total_score/3/ 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

#### Top List response
```bash
HTTP/1.0 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Date: Tue, 20 Dec 2016 14:52:35 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "avatar": null,
        "first_name": "Sergio",
        "last_name": "Infante Montero",
        "pk": 1,
        "username": "sinfante",
        "value": 40
    },
    {
        "avatar": null,
        "first_name": "pedro",
        "last_name": "carrillo chero",
        "pk": 3,
        "username": "pcarrillo",
        "value": 38
    },
    {
        "avatar": "/media/avatar/jnunez1482163617.jpg",
        "first_name": "Alex",
        "last_name": "Nuñez",
        "pk": 24,
        "username": "jnunez",
        "value": 24
    }
]
```

Logout
======

**/api/employee/logout/**

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/logout/ -H 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

* Using postman:

![Employee logout using POSTMAN](http://i.imgur.com/wfxPGjX.png 'Employee logout using POSTMAN')

* Using httpie:

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/logout/ 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

#### Logout response
```bash
HTTP/1.0 202 Accepted
Allow: OPTIONS, GET
Content-Type: application/json
Date: Tue, 20 Dec 2016 15:30:24 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Cookie
X-Frame-Options: SAMEORIGIN

{
    "detail": "User logout successfully"
}
```

Location List
=============

**/api/employee/location/list/**

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/location/list/ -H 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

* Using postman:

![Employee location list using POSTMAN](http://i.imgur.com/XF7OAIM.png 'Employee location list using POSTMAN')

* Using httpie:

```bash
http GET http://localhost:8000/api/employee/location/list/ 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

#### Location List response
```bash
HTTP/1.0 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Date: Tue, 20 Dec 2016 15:44:39 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "icon": "https://i.imgur.com/XRRUt6D.png",
        "name": "Buenos Aires",
        "pk": 3
    },
    {
        "icon": "https://i.imgur.com/CpYIGjr.png",
        "name": "Lima",
        "pk": 1
    },
    {
        "icon": "https://i.imgur.com/XRRUt6D.png",
        "name": "Mendoza",
        "pk": 2
    },
    {
        "icon": "https://i.imgur.com/A7Jdujn.png",
        "name": "USA",
        "pk": 4
    }
]
```

Role list
=========

**/api/employee/role/list/**

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/role/list/ -H 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

* Using postman:

![Employee role list using POSTMAN](http://i.imgur.com/gXZYcor.png 'Employee role list using POSTMAN')

* Using httpie:

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/role/list/ 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

#### Role List response
```bash
HTTP/1.0 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Date: Mon, 02 Jan 2017 21:18:59 GMT
Server: WSGIServer/0.1 Python/2.7.12
Vary: Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "name": "Developer",
        "pk": 1
    },
    {
        "name": "Notifier",
        "pk": 3
    },
    {
        "name": "QA",
        "pk": 2
    }
]
```

Reset Password
==============

**/api/employee/reset/password/{employee_email}/**

| Parameter        | Description                                                           |
|------------------|-----------------------------------------------------------------------|
| {employee_email} | Email address associated to employee username in registration process |

* Using curl:

```bash
curl -X GET https://bxconnect.herokuapp.com:443/api/employee/reset/password/sinfante@belatrixsf.com/ -H 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

* Using postman:

![Employee reset password using POSTMAN](http://i.imgur.com/W7xACAc.png 'Employee reset password using POSTMAN')

* Using httpie:

```bash
http GET https://bxconnect.herokuapp.com:443/api/employee/reset/password/sinfante@belatrixsf.com/ 'Authorization: Token 9f04499a53c148dab458109e3e3cb08e6a7a4b63'
```

#### Reset password response
```bash
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Connection: keep-alive
Content-Type: application/json
Date: Tue, 20 Dec 2016 19:01:11 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "detail": "Confirmation email sent.",
    "email": "sinfante@belatrixsf.com",
    "reset_password_code": "da4446c2-1786-496f-a9c6-64b661f98d4a"
}

```

Reset Password Confirmation
===========================

**/api/employee/reset/password/{employee_email}/{employee_uuid}/**

| Parameter        | Description                                                                         |
|------------------|-------------------------------------------------------------------------------------|
| {employee_email} | Email address associated to employee username in registration process               |
| {employee_uuid}  | UUID employee number, you will get that number in reset password confirmation email |


* Using curl:

```bash
curl -X GET https://belatrix-connect.herokuapp.com/api/employee/reset/password/sinfante@belatrixsf.com/93d9f4db-d06f-4dd3-b6d0-e87a40aacefe
```

* Using postman:

![Employee reset password confirmation using POSTMAN](http://i.imgur.com/S2fHQUN.png 'Employee reset password confirmation using POSTMAN')

* Using httpie:

```bash
http GET https://belatrix-connect.herokuapp.com/api/employee/reset/password/sinfante@belatrixsf.com/93d9f4db-d06f-4dd3-b6d0-e87a40aacefe
```

#### Reset Password Confirmation response

```bash
HTTP/1.1 200 OK
Allow: GET, OPTIONS
Connection: keep-alive
Content-Type: text/html; charset=utf-8
Date: Tue, 20 Dec 2016 19:56:35 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

<h1>Successfully password creation, email has been sent.</h1>

```
