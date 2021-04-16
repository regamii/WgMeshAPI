# Token
Used to get an JWT for a registered user. A token is **valid for 1 Hour**

- **URL** : `/token`
- **Method** : `GET`
- **Basic access authentication** : `<username>:<password>`
- **Auth** : `WWW-Authenticate: Basic realm="Authentication Required"`

## Example Call
In this example a token will be fetched for a registered user: username = `user`, password = `secret`.

```sh
curl -X GET -u "user:secret" http://wgmeshapi/api/token
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U"
}
```

## Error Response
- **Code** : `401 UNAUTHORIZED`
- **Content-Type** : `text/html`
- **Content** :

```html
Unauthorized Access
```
