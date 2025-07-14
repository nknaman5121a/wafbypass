
import requests
import hashlib

def send_requests(base_url, payloads):
    results = []
    for payload in payloads:
        url = base_url.replace("FUZZ", payload)
        try:
            r = requests.get(url, timeout=5)
            results.append({
                'payload': payload,
                'status': r.status_code,
                'hash': hashlib.md5(r.text.encode()).hexdigest(),
                'length': len(r.text),
                'url': url,
                'location': r.headers.get('Location')
            })
        except Exception as e:
            results.append({
                'payload': payload,
                'status': 'error',
                'error': str(e),
                'url': url
            })
    return results