import http.client
import json
import sys
import os

"""
pytreafik reads the treafik configuration, updates it with the data stored its config file then exists
"""

if __name__ == '__main__':
    TRAEFIK_CONFIG = os.getenv('TRAEFIK_CONFIG', '/etc/traefik.conf')
    TRAEFIK_HOST = os.getenv('TRAEFIK_HOST', '127.0.0.1')
    TRAEFIK_PORT = os.getenv('TRAEFIK_PORT', 8080)
    TRAEFIK_CONF_READ_ENDPOINT = os.getenv('TRAEFIK_CONF_READ_ENDPOINT', '/api/providers/rest')
    TRAEFIK_CONF_WRITE_ENDPOINT = os.getenv('TRAEFIK_CONF_WRITE_ENDPOINT', '/api/providers/rest')
    headers = {
        'Content-type': 'application/json'
    }
    conn = http.client.HTTPConnection(TRAEFIK_HOST, TRAEFIK_PORT)
    conn.request('GET', TRAEFIK_CONF_READ_ENDPOINT, headers=headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conf = json.loads(data.decode('utf-8'))
    try:
        with open(TRAEFIK_CONFIG, 'r') as f:
            new_conf = json.loads(f.read())
            conf.update(new_conf)
    except Exception as e:
        print(e)
        sys.exit(1)
    body = json.dumps(conf)
    conn.request('PUT', TRAEFIK_CONF_WRITE_ENDPOINT, body, headers=headers)
    response = conn.getresponse()
    print(response.status)
    sys.exit(0 if response.status == 200 else 1)
