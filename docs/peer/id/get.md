# List specific peer from specific network address
Get and list a specific peer from specific network address.

- **URL** : `/netaddr/<int:id>/peer/<int:id>`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example a specific peer from a specific network address will be fetched. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/netaddr/1/peer/1
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "id": 1,
    "user_id": 2,
    "name": "Netaddr1Peer1",
    "address": "10.1.0.1/16",
    "endpoint": "192.168.0.100:58120",
    "pubkey": "ejnBYSmh6UNWVF/Ct/+Ju/SxiaioBdUGBHBzlYMwpyU="
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
