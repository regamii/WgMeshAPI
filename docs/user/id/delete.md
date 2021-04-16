# Delete specific user
Delete specific registered user, **admin only**.

- **URL** : `/user/<int:id>`
- **Method** : `DELETE`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example an existing user is deleted by the admin account. In this example the JWT belongs to the admin user. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X DELETE -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/user/2
```

## Success Response
- **Code** : `204 NO CONTENT`
- **Content-Type** : `application/json`

## Error Response
- **Code** : `404 NOT FOUND`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
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
