# Generate WireGuard configuration specific to a peer.
Generate WireGuard configuration specific to a peer.

- **URL** : `/netaddr/<int:id>/peer/<int:id>/config`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example a WireGuard config will be generated for a specific peer in a specific network address. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT acquired from the `/token` endpoint.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/netaddr/1/peer/1/config
```

## Success Response
- **Code** : `200 OK`
- **Content-Type** : `text/plain`

```
[Interface]
# Network: Netaddr1
# Name: Netaddr1Peer1
Address = 10.1.0.1/16
ListenPort = 58120
PrivateKey = PLACEHOLDER

[Peer]
# Network: Netaddr1
# Name: Netaddr1Peer2
PublicKey = rleF/wK92zGAa0FeAhOeUPDVT1wqeUia/Vz6Df1BkmE=
AllowedIPs = 10.1.0.2/32
Endpoint = 192.168.0.101:58120

[Peer]
# Network: Netaddr1
# Name: Netaddr1Peer3
PublicKey = yGP4VpAIAH2yigxqTGPsdVvDWvcKE6nRU+iTm57gGkI=
AllowedIPs = 10.1.0.3/32
Endpoint = 192.168.0.102:58120
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
