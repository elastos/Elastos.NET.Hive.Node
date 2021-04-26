# Hive node manage
## Get hive node version
* Method: GET
* Endpoint: /api/v2/hive/version
* Response:
    - HTTP/1.1 200
    - version: hive node version
* Example:
    ```YAML
    Request:
        GET /api/v2/vault/backup/local/activate
    Response:
        HTTP/1.1 200
        {
            "version": "1.0.0"
        }
    ```

## Get commit hash 
* Endpoint: /api/v2/hive/commithash
* Method: GET
* Response:
    - HTTP/1.1 200
    - commit_hash: git commit hash
* Example:
    ```YAML
    Request:
        GET /api/v2/hive/commithash
    Response:
        HTTP/1.1 200
        {
            "commit_hash": "279b15650a86b16dcba289e74a09290ff225c69a"
        }
    ```
