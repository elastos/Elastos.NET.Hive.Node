# Service manage

## create free vault service
```YAML
Method: PUT
Endpoint: /api/v2/service/vault
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 201
    if vault exist, it will return
    - HTTP/1.1 200
Error-Code:
    (UNAUTHORIZED, "auth failed")

```

## remove vault service
```YAML
Method: DELETE
Endpoint: /api/v2/service/vault
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 204
Error-Code:
    (UNAUTHORIZED, "auth failed")
```

## freeze vault service
```YAML
Method: POST
Endpoint: /api/v2/service/vault/freeze 
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
Error-Code:
    (UNAUTHORIZED, "auth failed")
```

## unfreeze vault service
```YAML
Method: POST
Endpoint: /api/v2/service/vault/unfreeze 
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
Error-Code:
    (UNAUTHORIZED, "auth failed")
```

## Get vault service info 
```YAML
Method: GET
Endpoint: api/v2/service/vault
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
        {
            "did": "did:elastos:ij8krAVRJitZKJmcCufoLHQjq7Mef3ZjTN",
            "max_storage": 500, // Max 500 Mb storage size
            "file_use_storage": 100, // user have used 100 Mb in file storage size
            "db_use_storage": 50, // user have used 100 Mb in db storage size
            "modify_time": 1602236316,
            "start_time": 1602236316,
            "end_time": 1604914928,
            "pricing_using": "Rookie", // vault plan
            "state": "running" // running, freeze
        }

Error-Code:
    (UNAUTHORIZED, "auth failed")
    (NOT_FOUND, "vault service not found")
```

## create free backup service
```YAML
Method: PUT
Endpoint: /api/v2/service/backup
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 201
    if vault exist, it will return
    - HTTP/1.1 200
Error-Code:
    (UNAUTHORIZED, "auth failed")
```

## remove backup service
```YAML
Method: DELETE
Endpoint: /api/v2/service/backup
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 204
Error-Code:
    (UNAUTHORIZED, "auth failed")
```

## Get backup service info 
```YAML
Method: GET
Endpoint: /api/v2/service/backup
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
        { 
            "did": "did:elastos:ij8krAVRJitZKJmcCufoLHQjq7Mef3ZjTN",
            "backup_using": "Rookie",// backup plan
            "max_storage": 500, // Max 500 Mb backup storage size
            "use_storage": 10, // have used 100 Mb backup storage size
            "modify_time": 1602236316,
            "start_time": 1602236316,
            "end_time": 1604914928,
        }
Error-Code:
    (UNAUTHORIZED, "auth failed")
    (NOT_FOUND, "vault backup service not found")
```



