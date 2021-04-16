# WgMeshAPI Documentation
All API endpoints are housed under the `/api` prefix. In the examples the API is hosted at `http://wgmeshapi/` and cURL is used for example calls

## Open Endpoints
Open endpoints require no authenticating
 - [Token](token.md) : `GET /token`

## Endpoints that require Authentication
Closed endpoints require a valid JWT to be included in the `x-access-token` header. A token can be acquired from the Token view above.

### User
Each of the endpoints below manipulates or displays information about users. Based on the users token authorization level is determined.
- [List all users](user/get.md) : `GET /user`
- [Create user](user/post.md) : `POST /user`
- [List specific user](user/id/get.md) : `GET /user/<int:id>`
- [Alter specific user](user/id/put.md) : `PUT /user/<int:id>`
- [Delete specific user](user/id/delete.md) : `DELETE /user/<int:id>`

### Netaddr
Each of the endpoints below manipulates or displays information about network addresses. Peers, list below, will belong to a specific network address.
- [List all network addresses](netaddr/get.md) : `GET /netaddr`
- [Create network address](netaddr/post.md) : `POST /netaddr`
- [List specific network address](netaddr/id/get.md) : `GET /netaddr/<int:id>`
- [Alter specific network address](netaddr/id/put.md) : `PUT /netaddr/<int:id>`
- [Delete specific network address](netaddr/id/delete.md) : `DELETE /netaddr/<int:id>`

### Peer
Each of the endpoints below manipulates or displays information about peers. Each peer is tied to a specific network address, in a **one-to-many**. One network address can have many peers.
- [List all network address specific peers](peer/get.md) : `GET /netaddr/<int:id>/peer`
- [Create network address specific peer](peer/post.md) : `GET /netaddr/<int:id>/peer`
- [List specific peer from specific network address](peer/id/get.md) : `GET /netaddr/<int:id>/peer/<int:id>`
- [Alter specific peer from specific network address](peer/id/put.md) : `PUT /netaddr/<int:id>/peer/<int:id>`
- [Delete specific peer from specific network address](peer/id/delete.md) : `DELETE /netaddr/<int:id>/peer/<int:id>`
- [Generate WireGuard configuration specific to a peer](peer/id/config.md) : `GET /netaddr/<int:id>/peer/<int:id>/config`
