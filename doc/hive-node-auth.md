# Hive node auth 
## Sign In
* Endpoint: /api/v2/did/signin
* Method: POST
* Content-Type: "application/json"
* Request-Body:
    - id: the user’s DID document
* Response:
    - HTTP/1.1 200
    - challenge: the authentication challenge encoded in JWT
* Example:
    ```YAML
    Request:
        POST /api/v2/did/signin
        {
            "id": did_document
        }
    Response:
        HTTP/1.1 200
        {
            "challenge": jwt_data,
        }
    ```
## User auth
* Endpoint: /api/v2/did/auth
* Method: POST
* Content-Type: "application/json"
* Request-Body: 
    - challengeResponse: the response for the authentication challenge encoded in JWT
* Response:
    - HTTP/1.1 201
    - token: the access token encoded in JWT
* Example:
    ```YAML
    Request: 
        POST /api/v2/did/auth
        {"challengeResponse": "auth_token"}
    Response:
        HTTP/1.1 202 Accepted
        {
          "access_token": access_token,
        }
    ```

