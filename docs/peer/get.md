# List all network address specific peers
Get and list all peers from a specific network address.

- **URL** : `/netaddr/<int:id>/peer`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example all peers from a specific network address will be fetched. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/netaddr/1/peer
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "1": {
        "friendlyname": "Netaddr1Peer1",
        "address": "10.1.0.1/16",
        "endpoint": "192.168.0.100:58120",
        "pubkey": "ejnBYSmh6UNWVF/Ct/+Ju/SxiaioBdUGBHBzlYMwpyU=",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJrZXkiOiIxMDAifQ.jeZglKo-MJthVfBYtAl1suGU6S5vtuT6rFP-DaFkUZA"
    },
    "2": {
        "friendlyname": "Netaddr1Peer2",
        "address": "10.1.0.2/16",
        "endpoint": "192.168.0.101:58120",
        "pubkey": "rleF/wK92zGAa0FeAhOeUPDVT1wqeUia/Vz6Df1BkmE=",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJrZXkiOiIxMDEifQ.IcAchmrt1wBZPzQMSJ13ksWkFnnhYdJLupUpA5A7gaA"
    },
    "3": {
        "friendlyname": "Netaddr1Peer3",
        "address": "10.1.0.3/16",
        "endpoint": "192.168.0.102:58120",
        "pubkey": "yGP4VpAIAH2yigxqTGPsdVvDWvcKE6nRU+iTm57gGkI=",
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJrZXkiOiIxMDIifQ.590lA9u6JtoJkAYBIOXDWrdjewqmlMCYBenKI6JNOCk"
    }
}
```

## Error Response
- **Code** : `404 NOT FOUND`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

- **Code** : `401 UNAUTHORIZED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "Unauthorized"
}
```

- **Code:** : `401 UNAUTHORIZED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "Token is invalid"
}
```
