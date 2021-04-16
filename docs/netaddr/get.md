# List all network addresses
Get and list all network addresses.

- **URL** : `/netaddr`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example all network addresses will be fetched. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/netaddr
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "1": {
        "description": "Network1",
        "netaddr": "10.1.0.0/16"
    },
    "2": {
        "description": "Network2",
        "netaddr": "10.2.0.0/16"
    },
    "3": {
        "description": "Network3",
        "netaddr": "10.3.0.0/16"
    }
}
```

## Error Response
- **Code** : `401 UNAUTHORIZED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "Token is missing"
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
