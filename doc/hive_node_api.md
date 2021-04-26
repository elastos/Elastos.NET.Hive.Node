# Hive node plus plus api

## Table of Contents
- [Hive node manage](./hive-node-manage.md)
- [Hive Auth](./hive-node-auth.md)
- [Hive Payment](./hive-node-payment.md)
- [Hive Service](./hive-node-service.md)
- [Vault Database](./hive-node-vault-db.md)
- [Vault File](./hive-node-vault-file.md)
- [Vault Scripting](./hive-node-scripting.md)
- [Vault backup](hive-node-backup.md)

## Response uniform format
- Success:
    - HTTP/1.1 statue_code: 2xx, 3xx
    - Json body
        {
          "data": "json code",
        }
    - stream data
- Failure:
    HTTP/1.1 status_code: 4xx, 5xx
    - Json body
        {
            "error": {
                "code": 401,//internal error code
                "message": "error message",
            }
        }
    - text body
        exception which can not catch
