# WgMeshAPI
REST API for configuring WireGuard in a Mesh

## What is WgMeshAPI?
**Wg** short for [WireGuard](https://www.wireguard.com/) simple modern and fast VPN. **Mesh** in networking terms is a topology where every node has a connection to the all other nodes in a network. This means that in a mesh network every node can contact eachother, no restrictions. Partially Connected Mesh Network has been taken into consideration, but it adds a level of complexity. **API** Application Programming Interface.

## Why WgMeshAPI?
Why WgMeshAPI when there are probably better tools like k4yt3x/wg-meshconfig and costela/wesher https://github.com/search?utf8=%E2%9C%93&q=wireguard%20mesh? With an API clients can manage their own configurations. Why is this useful? With a tool like [k4yt3x/wg-meshconfig](https://github.com/k4yt3x/wg-meshconf) you install the tool locally, and configs are generated locally. When you've generated the configugration the next step is to find a way to efficiently and securely give the nodes the configurations. This is NOT a huge problem, but in my opinion it would be better if a client can download new configurations from a secure location.

## What about security?
If the API holds all the data it will be valuable target. WireGuard uses [Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography) meaning there is a public and private key. The public key you can give to others, like the API. The API will only hold public keys. With public keys and connection information WireGuard peers can be generated, and the `[Interface]` section partly generated.

When a node fetches configuration from the API it can be instructed on the client side to add the private key, stored locally, to the configuration. No node can use the configuration of a random peer because this node does not have the proper private key belonging to the public key. Hijacking is only possible if the attacker has the private key of one of the nodes.

## ToDo
- **API resources documentation**
- **Deployment documentation**
- **Create Docker file**
- **OpenAPI specification**
- **Read-only accounts** currently there is only a distinction between an admin and a normal account.
- **Read-only accounts for peers** currently peers do not have an account, and are forced now to use read/write accounts.
- **Better implement user roles and permissions**
