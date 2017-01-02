
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
