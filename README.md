# WgMeshAPI
REST API for configuring WireGuard in a Mesh

## What is WgMeshAPI?
**Wg** short for [WireGuard](https://www.wireguard.com/) simple modern and fast VPN. **Mesh**, in networking terms, is a topology where every node has a connection to the all other nodes in a network. This means that in a mesh network every node can contact each other, no restrictions. Partially Connected Mesh Network has been taken into consideration, but it adds a level of complexity. **API** Application Programming Interface.

## Why WgMeshAPI?
Why WgMeshAPI when there are probably better tools like k4yt3x/wg-meshconfig and costela/wesher https://github.com/search?utf8=%E2%9C%93&q=wireguard%20mesh? With an API, clients can manage their own configurations. **Why is this useful?** With a tool like [k4yt3x/wg-meshconfig](https://github.com/k4yt3x/wg-meshconf) you install the tool locally, and configurations are generated locally. When you've generated the configuration the next step is to find a way to efficiently and securely give the nodes the configurations. This is **NOT** a huge problem, but in my opinion it would be better if a client can download new configurations from a secure location.

## What about security?
If the API holds all the data it will be valuable target. WireGuard uses [Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) meaning there is a public and private key. The public key you can give to others, like the API. The API will only hold public keys. With public keys and connection information WireGuard peers can be generated, and the `[Interface]` section partly generated.

When a node fetches configuration from the API it can be instructed on the client side to add the private key, stored locally, to the configuration. No node can use the configuration of a random other peer because it does not have the proper private key belonging to the public key. Hijacking is only possible if the attacker has the private key of one of the nodes.

### Authorization
#### Admin
When there are no users in the database an admin account, first user in the database, can be set up at the root `/` of the site. This admin account can: create, read, update and delete other users. **How are other users distinguished from the admin account?** The API distinguishes users by position in the database. The admin is the first in the database, and thus if you are not first in the database you are NOT the admin.

#### Users
Users have been created by the admin account, and have: update, read and delete permission of their own account. User account can fully manipulate the netaddr and peer resources.

#### Peers
Peers are distinguished by their relationship to peer database table. Peers can only read the config endpoint.

### Authentication
All endpoints require a [JWT](https://en.wikipedia.org/wiki/JSON_Web_Token) to be accessible. To get an JWT access token one is required to send username and password to the `/token` endpoint. If the right username and password are supplied an JSON response will be sent back with an access token.

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U"
}
```

Authenticating to token required endpoints can be done by setting the `x-access-token` HTTP header to the JWT access token.

```sh
curl -X GET -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjE2ODQ2MTk5LjY2OTg4MTZ9.CMUrx135QNlUH0NsKO8rXg724dcQjhHPuPyptBwxP4U" {URL}
```

### API Documentation
API Reference can be found [here](docs/README.md).

## ToDo
- **API resources documentation**
- **Deployment documentation**
- **Create Docker file**
- **OpenAPI specification conformity**
- **Extensively test the API for potential misbehavior**
