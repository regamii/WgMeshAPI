# Generate a WireGuard configuration.
Generate WireGuard configuration specific to a peer.

- **URL** : `/config`
- **Method** : `GET`
- **Auth** : `x-access-token: <jwt>`

## Example Call
In this example a WireGuard config will be generated for a specific peer. In `x-access-token: <jwt>`, `<jwt>` is replaced with a JWT Token of a peer.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" http://wgmeshapi/api/config
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
- **Code** : `401 UNAUTHORIZED`
- **Content-Type** : `application/json`
- **Content** :

```json
{
    "message": "Peer token required"
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
