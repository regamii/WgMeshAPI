# List all users
Get and list all registered users.

- **URL** : `/user`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example all registered users will be fetched. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/user
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "1": {
        "username": "user",
        "admin": true
    },
    "2": {
        "username": "user1",
        "admin": false
    },
    "3": {
        "username": "Peer 1",
        "admin": false
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
