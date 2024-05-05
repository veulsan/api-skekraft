# Skellefteå Kraft API
This is a simple API for Skellefteå Kraft and requires username & password as a login method
.
If you do not have it you can go to mina sidor, https://minasidor.skekraft.se/login, login with bankid and create one by going to **Mitt Konto** and then **Inloggning**.

### Examples
Simple example on how to login with username & password:

```python
from api import SkekraftAPI
import asyncio

base_url = "https://externalapi.skekraft.se/api/MySkekraft"
skekraft_api = SkekraftAPI(base_url)
login_response = await skekraft_api.login("username", "password")
if login_response is not None and int(login_response['ErrNumber']) == 1:
    print(f"Login successful. Token: {login_response['Dst']}")
else:
    print(f"Login Failed: {login_response['ErrDescription']}")
    await skekraft_api.logout()
    exit(-1)
        login_response = await skekraft_api.login("username", "password")

```

You can also use a token if you have one. Do remember to refresh it regurlary do not invalide it:

```python
from api import SkekraftAPI
import asyncio

base_url = "https://externalapi.skekraft.se/api/MySkekraft"
skekraft_api = SkekraftAPI(base_url)
token = "your-token-here"
token = await skekraft_api.refresh(token)
log(f"Response: {token}")
```
See example.py for more examples details on how it can be used
