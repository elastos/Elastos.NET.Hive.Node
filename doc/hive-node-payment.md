# Payment

## Get payment version 
```YAML
Method: GET 
Endpoint: /api/v2/payment/version
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

        {
            
            "version": "1.0"
        }

Error-Code:
    (UNAUTHORIZED, "auth failed")
    (BAD_REQUEST, "vault does not exist.")
    (BAD_REQUEST, "vault have been freeze, can not write")
    (BAD_REQUEST, "not enough storage space")
```

## Get pricing plan info of all service  
```YAML
Method: GET
Endpoint: /api/v2/payment/pricingplan/all
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
        {
        "backupPlans": [
        {
        "amount": 0,
        "currency": "ELA",
        "maxStorage": 500,
        "name": "Free",
        "serviceDays": -1
        },
        {
        "amount": 1.5,
        "currency": "ELA",
        "maxStorage": 2000,
        "name": "Rookie",
        "serviceDays": 30
        },
        {
        "amount": 3,
        "currency": "ELA",
        "maxStorage": 5000,
        "name": "Advanced",
        "serviceDays": 30
        }
        ],
        "paymentSettings": {
        "receivingELAAddress": "ETJqK7o7gBhzypmNJ1MstAHU2q77fo78jg",
        "wait_payment_timeout": 30,
        "wait_tx_timeout": 120
        },
        "pricingPlans": [
        {
        "amount": 0,
        "currency": "ELA",
        "maxStorage": 500,
        "name": "Free",
        "serviceDays": -1
        },
        {
        "amount": 2.5,
        "currency": "ELA",
        "maxStorage": 2000,
        "name": "Rookie",
        "serviceDays": 30
        },
        {
        "amount": 5,
        "currency": "ELA",
        "maxStorage": 5000,
        "name": "Advanced",
        "serviceDays": 30
        }
        ],
        "version": "1.0"
        }

Error-Code:
(UNAUTHORIZED, "auth failed")
```

## Get vault service pricing plan by name
```YAML
Method: GET 
Endpoint: /api/v2/payment/pricingplan/vault?name=<name>
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

        {
            
            "name": "Rookie",
            "maxStorage": 2000,
            "serviceDays": 30,
            "amount": 2.5,
            "currency": "ELA"
        }

Error-Code:
    (UNAUTHORIZED, "auth failed") 
    (BAD_REQUEST, "parameter is null")
    (NOT_FOUND, "not found pricing name")
```

## Get backup service pricing plan by name
```YAML
Method: GET 
Endpoint: /api/v2/payment/pricingplan/backup?name=<name>
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200
        {
            "name": "Rookie",
            "maxStorage": 2000,
            "serviceDays": 30,
            "amount": 2.5,
            "currency": "ELA"
        }
Error-Code:
    (UNAUTHORIZED, "auth failed") 
    (BAD_REQUEST, "parameter is null")
    (NOT_FOUND, "not found backup name")
```

## Create payment order
```YAML
Method: POST
Endpoint: /api/v2/payment/package_order/create
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
      "pricing_name": "Rookie",
    } 
    to create a vault service order
    {
      "backup_name": "Rookie",
    } 
    to create a vault backup service order

Response:
    - HTTP/1.1 200
      {
        "order_id": "5f910273dc81b7a0b3f585fc"
      }
Error-Code:
    (UNAUTHORIZED, "auth failed")
    (NOT_FOUND, "not found pricing_name of:" + content["pricing_name"])
    (NOT_FOUND, "not found backup_name of:" + content["backup_name"])
    (BAD_REQUEST, "parameter pricing_name and backup_name is null")
```

## Pay vault service package order
```YAML
Method: POST
Endpoint: /api/v2/payment/package_order/pay
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
      "order_id": "5f910273dc81b7a0b3f585fc",
      "pay_txids": [
        "0xablcddd",
        "0xablcdef"
      ]
    }
Response:
    - HTTP/1.1 200

      {
        
      }

Error-Code:
    (UNAUTHORIZED, "auth failed")
    (BAD_REQUEST, "parameter is not application/json")
    (BAD_REQUEST, "parameter is null")
    (BAD_REQUEST, "txid has been used")
```

## Get order info 
```YAML
Method: GET
Endpoint: /api/v2/payment/package_order?order_id=<order_id>
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

        {
            
            "order_info":
            { 
                "order_id":"5f910273dc81b7a0b3f585fc", 
                "did":"did:elastos:ioLFi22fodmFUAFKia6uTV2W8Jz9vEcQyP",
                "app_id":"appid",
                "pricing_info":{
                    "name": "Rookie",
                    "maxStorage": 2000,
                    "serviceDays": 30,
                    "amount": 2.5,
                    "currency": "ELA"
                },
                "pay_txids": [
                    "0xablcddd",
                    "0xablcdef"
                ],
                "state": "wait_tx",//wait_pay, wait_tx, wait_pay_timeout, wait_tx_timeout, failed, success
                "type": "backup", // vault, backup
                "creat_time": 1602236316,
                "finish_time": 1602236366
            }
        }

Error-Code:
    (UNAUTHORIZED, "auth failed")
    (BAD_REQUEST, "parameter is not application/json")
    (BAD_REQUEST, "parameter is null")
```

## Get history of order info list 
```YAML
Method: GET
Endpoint: /api/v2/payment/package_order/history
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

        {
            
            "order_info_list":[
                { 
                    "order_id":"5f910273dc81b7a0b3f585fc", 
                    "did":"did:elastos:ioLFi22fodmFUAFKia6uTV2W8Jz9vEcQyP",
                    "app_id":"appid",
                    "pricing_info":{
                        "name": "Rookie",
                        "maxStorage": 2000,
                        "serviceDays": 30,
                        "amount": 2.5,
                        "currency": "ELA"
                    },
                    "pay_txids": [
                        "0xablcddd",
                        "0xablcdef"
                    ],
                    "type": "vault",
                    "state": "wait_tx",//wait_pay, wait_tx, wait_pay_timeout, wait_tx_timeout, failed, success 
                    "creat_time": 1602236316,
                    "finish_time": 1602236366
                }
            ]
        }

Error-Code:
    (UNAUTHORIZED, "auth failed")
```

