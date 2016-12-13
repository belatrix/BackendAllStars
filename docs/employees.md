Employees API documentation!
============================

Employees endpoints.

Authenticatication
==================

**/api/employee/authenticate/**

* Using curl:

```bash
curl -X POST -d "username=sinfante&password=allstars" https://bxconnect.herokuapp.com:443/api/employee/authenticate/
```

* Using postman:

[Authentication using POSTMAN](http://i.imgur.com/TP009D3.png 'Authentication using POSTMAN')

* Using httpie:

```bash
http -f POST https://bxconnect.herokuapp.com:443/api/employee/authenticate/ username='sinfante' password='allstars'
```
