import urllib.request
from urllib.parse import urlencode

def post_register(username, password):
    data = urlencode({'username': username, 'password': password}).encode()
    req = urllib.request.Request('http://127.0.0.1:5000/register', data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print('Status:', resp.getcode())
            print('Final URL:', resp.geturl())
            b = resp.read(200)
            print('Body (truncated):')
            print(b.decode('utf-8', errors='replace'))
    except Exception as e:
        print('Error during POST:', e)

if __name__ == '__main__':
    post_register('B_brannel', 'pass123')
