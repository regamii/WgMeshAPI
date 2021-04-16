# Create network address
Create a new network address.

- **URL** : `/netaddr`
- **Method** : `POST`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
description=<alphanumeric>&netaddr=<alphanumeric>
```

- **Data example**

```
description=Netaddr1&netaddr=10.1.0.0/16
```

## Example Call
In this example a new network address is created. In this example the JWT belongs to either a 'normal' user, or admin. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X POST -d "description=Netaddr1" -d "netaddr=10.1.0.0/16" -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/netaddr
```

## Success Response
- **Code** : `201 CREATED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "id": 1,
    "description": "Network1",
    "netaddr": "10.1.0.0/16"
}
```

## Error Response
- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "netaddr": "Virtual network address to use"
    }
}
```

- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "netaddr": "Virtual network address to use"
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
