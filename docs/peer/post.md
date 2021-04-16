# Create network address specific peer
Create a new peer specific to a network address.

- **URL** : `/netaddr/<int:id>/peer`
- **Method** : `POST`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
name=<alphanumeric>&address=<alphanumeric>&endpoint=<alphanumeric>&pubkey=<alphanumeric>&password=<alphanumeric>
```

- **Data example**

```
name=Netaddr1Peer1&address=10.1.0.1/16&endpoint=192.168.0.100:58120&pubkey=ejnBYSmh6UNWVF/Ct/%2BJu/SxiaioBdUGBHBzlYMwpyU=&password=secret
```

## Example Call
In this example a new network address is created. In this example the JWT belongs to either a 'normal' user, or admin. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X POST -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" -d "name=Netaddr1Peer1" -d "address=10.1.0.1/16" -d "endpoint=192.168.0.100:58120" -d "pubkey=ejnBYSmh6UNWVF/Ct/%2BJu/SxiaioBdUGBHBzlYMwpyU=" -d "password=secret" http://wgmeshapi/api/netaddr/1/peer
```

## Success Response
- **Code** : `201 CREATED`
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
