# Pub/Sub

## publish a pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/publish
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "channel_name": "some_talking_channel"
    } 
Response:
    - HTTP/1.1 200

      {
        
      }

```

## remove a pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/remove
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "channel_name": "some_talking_channel"
    } 
Response:
    - HTTP/1.1 200

      {
        
      }

```

## get this did and app_id publish channels
```YAML
Method: GET
Endpoint: /api/v2/vault/pubsub/pub/channels
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

      {
        
        channels = [
            "channel_1",
            "channel_2",
            "channel_3"
        ]
      }

```

## get this did and app_id subscribe channels
```YAML
Method: GET
Endpoint: /api/v2/vault/pubsub/sub/channels
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Response:
    - HTTP/1.1 200

      {
        
        channels = [
            "channel_1",
            "channel_2",
            "channel_3"
        ]
      }

```


## subscribe  a pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/subscribe
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "pub_did": "elastos:did:xxxxxxxx",
        "pub_app_id": "some data for appid",
        "channel_name": "some_talking_channel"
    } 
Response:
    - HTTP/1.1 200

      {
        
      }

```

## unsubscribe a pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/unsubscribe
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "pub_did": "elastos:did:xxxxxxxx",
        "pub_app_id": "some data for appid",
        "channel_name": "some_talking_channel"
    } 
Response:
    - HTTP/1.1 200

      {
        
      }

```

## push a message to pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/push
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "channel_name": "some_talking_channel",
        "message: "some message to publish"
    } 
Response:
    - HTTP/1.1 200

      {
        
      }

```

## get a message from pub/sub channel
```YAML
Method: POST
Endpoint: /api/v2/vault/pubsub/pop``
Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
Content-Type: "application/json"
Request-Body: 
    {
        "pub_did": "elastos:did:xxxxxxxx",
        "pub_app_id": "some data for appid",
        "channel_name": "some_talking_channel",
        "message_limit": 10
    } 
Response:
    - HTTP/1.1 200

        {
            
            "messages":[
                {"message":"message1", "time":1614919830},
                {"message":"message2", "time":1614919835}
            ]
        }

```
