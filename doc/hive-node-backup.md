# Vault Backup

## Backup hive vault to google drive
* Endpoint: /api/v2/vault/backup/google_drive/save
* Method: POST
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Request-Body:
    - The input data is google oauth2 token to json, no need to change anything. There is a sample code in python: oauth_google_desktop.py"
* Response:
    - HTTP/1.1 200
* Example:
    ```YAML
    Request:
        POST /api/v2/vault/backup/google_drive/save
        { 
            "token": "ya29.A0AfH6SMAuwGipoRVMVnvon_C_qqMhzpK53QzDQ8rapZavP_JXa8ASFecIKcKsy91oek8UvjbXfLMB9rlVG3Wj3X4e6drbNGuJjq97U8Lo6uwxwTpcmeybSl0wkQihwXZJlc3fKY31tvsT55vUbSSWwugPETCPZAFs2Oo_MURWbtY",
            "refresh_token": "1//06-2759fIGiJdCgYIARAAGAYSNwF-L9Irf7R8nimVqT2UieEcO5wtZMk1uNLxyBk_jB2WCPHDY7rhdTV_0WvHp5K09BWy1lUZnng",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "24235223939-guh47dijl0f0idm7h04bd44ulfcodta0.apps.googleusercontent.com",
            "client_secret": "mqaI40MlghlNkfaFtDBzvpGg",
            "scopes": ["https://www.googleapis.com/auth/drive"],
            "expiry": "2020-11-17T05:14:10Z"
        }
    Response:
        - HTTP/1.1 200
    ```

## Restore hive vault from google drive
* Endpoint: /api/v2/vault/backup/google_drive/restore
* Method: POST
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Request-Body:
    - The input data is google oauth2 token to json, no need to change anything. There is a sample code in python: oauth_google_desktop.py
* Response:
    - HTTP/1.1 200
* Example:
    ```YAML
    Request:
        POST /api/v2/vault/backup/google_drive/restore
        { 
            "token": "ya29.A0AfH6SMAuwGipoRVMVnvon_C_qqMhzpK53QzDQ8rapZavP_JXa8ASFecIKcKsy91oek8UvjbXfLMB9rlVG3Wj3X4e6drbNGuJjq97U8Lo6uwxwTpcmeybSl0wkQihwXZJlc3fKY31tvsT55vUbSSWwugPETCPZAFs2Oo_MURWbtY",
            "refresh_token": "1//06-2759fIGiJdCgYIARAAGAYSNwF-L9Irf7R8nimVqT2UieEcO5wtZMk1uNLxyBk_jB2WCPHDY7rhdTV_0WvHp5K09BWy1lUZnng",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "24235223939-guh47dijl0f0idm7h04bd44ulfcodta0.apps.googleusercontent.com",
            "client_secret": "mqaI40MlghlNkfaFtDBzvpGg",
            "scopes": ["https://www.googleapis.com/auth/drive"],
            "expiry": "2020-11-17T05:14:10Z"
        }
    Response:
        - HTTP/1.1 200
    ```

## Get backup state 
* Endpoint: /api/v2/vault/backup/state
* Method: GET
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
    - hive_backup_state:  backup or restore is running or stop.  stop, backup, restore
    - result": last backup or restore is success or failed
* Example:
    ```YAML
    Request:
        GET /api/v2/vault/backup/state
    Response:
        - HTTP/1.1 200
        {
            "hive_backup_state": "stop"// stop, backup, restore
            "result": "success" //success, failed
        }
    ```

## Backup hive vault to other hive node
* Method: POST
* Endpoint: /api/v2/vault/backup/node/save
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Request-Body:
    - backup_credential:issue by user did for hive node inter communicate, see detail in hive_auth_test.py:issue_backup_auth
* Response:
    - HTTP/1.1 200
* Example:
    ```YAML
    Request:
        POST /api/v2/vault/backup/node/save
        { 
            "backup_credential": "{\"id\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM#backupId\",\"type\":[\"BackupCredential\"],\"issuer\":\"did:elastos:icXtpDnZRSDrjmD5NQt6TYSphFRqoo2q6n\",\"issuanceDate\":\"2021-02-26T08:47:26Z\",\"expirationDate\":\"2026-02-26T08:47:26Z\",\"credentialSubject\":{\"id\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM\",\"sourceDID\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM\",\"targetDID\":\"did:elastos:iiTvjocqh7C78KjWyDVk2C2kbueJvkuXTW\",\"targetHost\":\"https://hive-testnet2.trinity-tech.io\"},\"proof\":{\"verificationMethod\":\"#primary\",\"signature\":\"6l48lIa25AfEGxtlH_AsGO2cKOZ7CzydP1f4Tyg7zom6QgKOQAyTxkey7_0B1L9ZejKgPjJU5t4OYrQ3uaVEdQ\"}}"
        }
    Response:
        - HTTP/1.1 200
    ```

## Restore hive vault from other hive node
* Endpoint: /api/v2/vault/backup/node/restore
* Method: POST
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Request-Body:
    - backup_credential:issue by user did for hive node inter communicate, see detail in hive_auth_test.py:issue_backup_auth
* Response:
    - HTTP/1.1 200
* Example:
    ```YAML
    Request:
        POST /api/v2/vault/backup/node/restore
        { 
            "backup_credential": "{\"id\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM#backupId\",\"type\":[\"BackupCredential\"],\"issuer\":\"did:elastos:icXtpDnZRSDrjmD5NQt6TYSphFRqoo2q6n\",\"issuanceDate\":\"2021-02-26T08:47:26Z\",\"expirationDate\":\"2026-02-26T08:47:26Z\",\"credentialSubject\":{\"id\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM\",\"sourceDID\":\"did:elastos:ijUnD4KeRpeBUFmcEDCbhxMTJRzUYCQCZM\",\"targetDID\":\"did:elastos:iiTvjocqh7C78KjWyDVk2C2kbueJvkuXTW\",\"targetHost\":\"https://hive-testnet2.trinity-tech.io\"},\"proof\":{\"verificationMethod\":\"#primary\",\"signature\":\"6l48lIa25AfEGxtlH_AsGO2cKOZ7CzydP1f4Tyg7zom6QgKOQAyTxkey7_0B1L9ZejKgPjJU5t4OYrQ3uaVEdQ\"}}"
        }
    Response:
        - HTTP/1.1 200
    ```

## Active hive backup data to vault
* Endpoint: /api/v2/vault/backup/local/activate
* Method: POST
* Authorization: "token 38b8c2c1093dd0fec383a9d9ac940515"
* Content-Type: "application/json"
* Response:
    - HTTP/1.1 200
* Example:
    ```YAML
        Request:
            POST /api/v2/vault/backup/local/activate
        Response:
            - HTTP/1.1 200
    ```
