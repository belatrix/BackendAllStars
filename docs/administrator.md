
Administrator endpoints.


Employee Bulk Creation
======================

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

#### Employee Bulk Creation Response

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

Employees Deactivated List
==========================

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

#### Employees Deactivated List response
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

Employee set Roles or Positions
===============================

**/api/admin/employee/{employee_id}/set/list/**

*Json input data structure:*

| Type     | Example                                  |
|----------|------------------------------------------|
| role     | {"type":"role","set_id_list":[1,2]}      |
| position | '{"type":"position","set_id_list":[1,2]} |

* Using curl:

```bash
curl -X PATCH -d '{"type":"role","set_id_list":[1,2]}' -H 'Authorization: Token b380acd402121d71b97cb1dad21574f1c7ca30cb' -H 'Content-Type: application/json' https://bxconnect.herokuapp.com:443/api/admin/employee/3/set/list/
```

* Using postman:

![Employee set roles or positions using POSTMAN 1](http://i.imgur.com/iT0bzwu.png 'Employee set roles or positions using POSTMAN 1')
![Employee set roles or positions using POSTMAN 2](http://i.imgur.com/bn3fLEP.png 'Employee set roles or positions using POSTMAN 2')

* Using httpie:

```bash
http PATCH https://bxconnect.herokuapp.com:443/api/admin/employee/3/set/list/ 'Authorization: Token b380acd402121d71b97cb1dad21574f1c7ca30cb' <<< '{"type":"role","set_id_list":[1,2]}'
```

#### Employees set Roles or Positions response
```bash
HTTP/1.1 202 Accepted
Allow: PATCH, OPTIONS
Connection: keep-alive
Content-Type: application/json
Date: Tue, 03 Jan 2017 17:30:35 GMT
Server: gunicorn/19.4.5
Transfer-Encoding: chunked
Vary: Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

{
    "avatar": null,
    "current_month_score": 0,
    "current_year_score": 0,
    "email": "pcarrillo@belatrixsf.com",
    "first_name": "pedro",
    "is_active": true,
    "is_admin": "True",
    "is_base_profile_complete": false,
    "is_blocked": false,
    "is_password_reset_required": true,
    "last_login": null,
    "last_month_score": 38,
    "last_name": "carrillo chero",
    "last_year_score": 0,
    "level": 0,
    "location": {
        "icon": "https://i.imgur.com/CpYIGjr.png",
        "id": 1,
        "name": "Lima"
    },
    "pk": 3,
    "positions": [
        {
            "name": "SME",
            "pk": 1,
            "weight": 3
        },
        {
            "name": "Team Leader / Team Manager",
            "pk": 2,
            "weight": 4
        },
        {
            "name": "Manager",
            "pk": 3,
            "weight": 5
        }
    ],
    "roles": [
        {
            "name": "Developer",
            "pk": 1
        },
        {
            "name": "QA",
            "pk": 2
        }
    ],
    "skype_id": "pcarrillo",
    "total_given": 0,
    "total_score": 38,
    "username": "pcarrillo"
}
```
