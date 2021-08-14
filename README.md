# flasksso

adludio sso authentication based route guard for flask

## Installation

```bash
pip3 install git+https://github.com:FutureAdLabs/flask-sso.git#egg=flask-sso
```

## Usage

`say-hello` endpoint is guarded by sso authentication

```python
from flasksso import SsoAuth

sso_auth = SsoAuth()

@app.route('/say-hello', methods=['GET'])
@sso_auth.required
def route_func():
    pass
```

Request make to guarded routes shoud contain a valid token

```typescript
fetch('/say-hello', {
  method: 'GET',
  headers: {
    'content-type': 'application/json',
    Authorization: `Bearer ${token}`,
    'Access-Origin': '*',
  },
});
```

## Authentication Fails!
If authentication fails, sso error response is returned
```json
{
  data: null,
  error: {
    message: string // Hint to describe
    status: number // Status code corresponding to HTTP Status codes,
    label: string // A programmatic error code
  }
}

```

