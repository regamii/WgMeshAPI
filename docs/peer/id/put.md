# Alter specific peer from specific network address
Alter a specific peer from a specific network address.

- **URL** : `/netaddr/<int:id>/peer/<int:id>`
- **Method** : `PUT`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
friendlyname=<alphanumeric>&address=<alphanumeric>&endpoint=<alphanumeric>&pubkey=<alphanumeric>
```

- **Data example**

```
friendlyname=Netaddr1Peer1&address=10.1.0.1/16&endpoint=192.168.0.200:58120&pubkey=YpGq46XWF909c7rJ4a7AzDtA4SUAKGzR4OW4JkbXrmg=
```

## Example Call
In this example an existing peer from a network address is altered. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X PUT -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" -d "friendlyname=Netaddr1Peer1" -d "address=10.1.0.1/16" -d "endpoint=192.168.0.100:58120" -d "pubkey=ejnBYSmh6UNWVF/Ct/%2BJu/SxiaioBdUGBHBzlYMwpyU=" http://wgmeshapi/api/netaddr/1
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "id": 1,
    "friendlyname": "Netaddr1Peer1",
    "address": "10.1.0.1/16",
    "endpoint": "192.168.0.200:58120",
    "pubkey": "YpGq46XWF909c7rJ4a7AzDtA4SUAKGzR4OW4JkbXrmg=",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJrZXkiOiIxMDAifQ.jeZglKo-MJthVfBYtAl1suGU6S5vtuT6rFP-DaFkUZA"
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

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "friendlyname": "Name of the peer"
    }
}
```

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "address": "IP address in the overlay network"
    }
}
```

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "endpoint": "Endpoint in the 'normal' network"
    }
}
```

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "pubkey": "Public key of this peer."
    }
}
```

- **Code** : `500 INTERNAL SERVER ERROR`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available."
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
