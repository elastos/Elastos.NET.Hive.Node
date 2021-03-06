# Hive node auth 
## User auth access request
```YAML
HTTP: POST
URL: /api/v1/did/sign_in
Content-Type: "application/json"
data: {"document": did_document}
return:
    Success:
        {
          "_status":"OK",
          "challenge": jwt,
        }
    Failure:
        {
          "_status": "ERR",
          "_error": {
            "code": 401,
            "message": err_message
          }
        }
comments: jwt include "nonce"
error code: 
    (UNAUTHORIZED, "parameter is not application/json")
    (BAD_REQUEST, "error message")
    (INTERNAL_SERVER_ERROR, "error message")

```
## User auth
```YAML
HTTP: POST
URL: /api/v1/did/auth
Content-Type: "application/json"
data: {"jwt": "auth_token"}
return:
    Success:
        {
          "_status":"OK",
          "access_token": access_token,
        }
    Failure:
        {
          "_status": "ERR",
          "_error": {
            "code": 401,
            "message": "err_message"
          }
        }
comments: access_token is a "token", and it is a jwt too.
error code: 
    (UNAUTHORIZED, "error message")
```

