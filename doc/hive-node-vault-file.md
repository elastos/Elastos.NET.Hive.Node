# Vault File
## Upload file
* Endpoint: /api/v2/vault/files/<path/to/res>
* Method: PUT
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Request-Body: 
    - file data
* Response:
    - HTTP/1.1 201
* Example
    ```YAML
        Request:
            PUT /api/v2/vault/files/some/path/of/file
            upload file data
        Response:
            HTTP/1.1 201 
    ```

## Download file
* Endpoint: /api/v2/vault/files/<path/to/res>
* Method: GET
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Request-Body: None
* Response:
    - HTTP/1.1 200
    - file data
* Example
    ```YAML
    Request:
        GET /api/v2/vault/files/some/path/of/file
    Response:
        HTTP/1.1 200
        file data
    ```

## Delete file or folder
* Endpoint: /api/v2/vault/files/<path/to/res>
* Method: DELETE 
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 204
* Example
    ```YAML
    Request:
        DELETE /api/v2/vault/files/some/path/of/file
    Response:
        HTTP/1.1 204
    ```

## Move file or folder
* Endpoint: /api/v2/vault/files/<path/to/res>?to=/path/to/dest
* Method: PATCH
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - name: new path of file
* Example:
    ```YAML
    Request:
        PATCH /api/v2/vault/files/some/path/of/file?to=/path/to/dest
    Response:
        HTTP/1.1 200
        {
          "name": "/path/to/dest"
        }
    ```

## Copy file or folder
* Endpoint: /api/v2/vault/files/<path/to/res>?dst=/path/to/dst
* Method: PUT
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - name: new file path
* Example:
    ```YAML
    Request:
        PUT /api/v2/vault/files/some/path/of/file?dst=/path/to/dst
    Response:
        HTTP/1.1 200
        {
          "name": "/path/to/dst"
        }
    ```

## Get properties of file or folder
* Endpoint: api/v2/vault/files/<path/to/res>?comp=metadata
* Method: GET
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - name: file name with full path
    - size: file size or folder size
    - updated: updated timestamp
    - created: created timestamp
* Example:
    ```YAML
        Request:
            GET /api/v2/vault/files/some/path/of/file?comp=metadata
        Response:
            HTTP/1.1 200
            {
                "name": "file_or_folder_name",
                "size": 230,
                "updated": "timestamp",
                "created": "timestamp"
            }
    ```

## List folder
* Endpoint: /api/v2/vault/files/<path/to/dir>?comp=children
* Method: GET
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - name: file name
    - size: file or folder size
    - is_file: true: file; false: folder.
* Example:
    ```YAML
        Request:
            GET /api/v2/vault/files/path/of/dir?comp=children
        Response:
        - HTTP/1.1 200
        [
            {
                "name": "file_name",
                "size": 230,
                "is_file": true
            },
            {
                "name": "folder_name",
                "size": 330,
                "is_file": false 
            },
        ]
    ```

## Get file hash(SHA256)
* Method: GET
* Endpoint: /api/v2/vault/files/<path/to/file>?comp=hash
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - name: file name
    - hash: file sha256 hash

* Example:
```YAML
        Request:
            GET /api/v2/vault/files/path/of/file?comp=hash
        Response:
        - HTTP/1.1 200
        {
            "name": "new-item-name.txt",
            "hash": "3a29a81d7b2718a588a5f6f3491b3c578a5f6f3491b3c578a5f6f3491b3c578a5f6f3491b3c57"
        }
```

