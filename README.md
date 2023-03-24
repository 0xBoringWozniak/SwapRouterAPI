# SwapRouterAPI

### Enviroments
In `env.txt`:
- HTTP_NODE: HTTP Node URL (e.g. http://localhost:5000) or infura URL (e.g. https://mainnet.infura.io/v3/...)
- MONGO_URI: Mongo URI to connect in format mongodb://<user>:<password>@<host>:<port>

### How to run?
```
docker build . -t swap_api:latest
docker run -p 8000:8000 --name=SWAP_API --env-file=env.txt -d swap_api:latest
```
