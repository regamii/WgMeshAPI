# Create peer on specific network address
Create a new peer on a specific network address.

- **URL** : `/netaddr/<int:id>/peer`
- **Method** : `POST`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
friendlyname=<alphanumeric>&address=<alphanumeric>&endpoint=<alphanumeric>&pubkey=<alphanumeric>
```

- **Data example**

```
friendlyname=Netaddr1Peer1&address=10.1.0.1/16&endpoint=192.168.0.100:58120&pubkey=ejnBYSmh6UNWVF/Ct/%2BJu/SxiaioBdUGBHBzlYMwpyU=
```

## Example Call
In this example a new peer is created in a specific network address. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X POST -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" -d "friendlyname=Netaddr1Peer1" -d "address=10.1.0.1/16" -d "endpoint=192.168.0.100:58120" -d "pubkey=ejnBYSmh6UNWVF/Ct/%2BJu/SxiaioBdUGBHBzlYMwpyU=" http://wgmeshapi/api/netaddr/1/peer
```

## Success Response
- **Code** : `201 CREATED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "id": 1,
    "friendlyname": "Netaddr1Peer1",
    "address": "10.1.0.1/16",
    "endpoint": "192.168.0.100:58120",
    "pubkey": "ejnBYSmh6UNWVF/Ct/+Ju/SxiaioBdUGBHBzlYMwpyU=",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJrZXkiOiIxMDAifQ.jeZglKo-MJthVfBYtAl1suGU6S5vtuT6rFP-DaFkUZA"
}
```

## Error Response
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
