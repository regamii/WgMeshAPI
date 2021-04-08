# Create a user
Create a new user, **admin only**.

- **URL** : `/user`
- **Method** : `POST`
- **Auth** : `x-access-token: <jwt>`
- **Content-Type** : application/x-www-form-urlencoded
- **Data constraints** :

```
username=<alphanumeric>&password=<alphanumeric>
```

- **Data example**

```
username=MyCoolUsername&password=MyCoolPassword
```

## Example Call
In this example a new user is created by the admin account. In this example the JWT belongs to the admin user. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X POST -d "username=MyCoolUsername" -d "password=MyCoolPassword" -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/user
```

## Success Response
- **Code** : `201 CREATED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "id": 2,
    "username": "MyCoolUsername",
    "admin": false
}
```

## Error Response
- **Code** : `400 BAD REQUEST`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": {
        "username": "Username is required"
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
    "message": "The action could not be successfully performed. This could be due to unique constraints in the database, or the database not being available"
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
