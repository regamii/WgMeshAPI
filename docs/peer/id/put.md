# Alter specific peer from specific network address
Alter a specific peer from a specific network address.

- **URL** : `/netaddr/<int:id>/peer/<int:id>`
- **Method** : `PUT`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
name=<alphanumeric>&address=<alphanumeric>&endpoint=<alphanumeric>&pubkey=<alphanumeric>&password=<alphanumeric>
```

- **Data example**

```
name=Netaddr1Peer1&address=10.1.0.1/16&endpoint=192.168.0.200:58120&pubkey=YpGq46XWF909c7rJ4a7AzDtA4SUAKGzR4OW4JkbXrmg=&password=secret
```

## Example Call
In this example an existing peer from a network address is altered by the a 'normal' user, or admin, account. In this example the JWT belongs to either a 'normal' user, or admin. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X PUT -d "description=Netaddr1" -d "netaddr=10.1.0.0/16" -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/netaddr/1
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
    "endpoint": "192.168.0.200:58120",
    "pubkey": "YpGq46XWF909c7rJ4a7AzDtA4SUAKGzR4OW4JkbXrmg="
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
        "name": "Name of the peer"
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

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "password": "Password is required"
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
