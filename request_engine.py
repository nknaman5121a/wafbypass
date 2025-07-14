import requests
import hashlib

def send_requests(base_url, payloads, verbose=False):
    results = []
    for payload in payloads:
        url = base_url.replace("FUZZ", payload)
        if verbose:
            print(f"[>] Sending payload: {payload}")
        try:
            r = requests.get(url, timeout=5, allow_redirects=True)
            results.append({
                'payload': payload,
                'status_code': r.status_code,
                'hash': hashlib.md5(r.text.encode()).hexdigest(),
                'length': len(r.text),
                'final_url': r.url,
                'location': r.headers.get('Location'),
                'content': r.text[:300]
            })
        except Exception as e:
            if verbose:
                print(f"[!] Error sending request for payload: {payload}\n    └─ {repr(e)}")
            results.append({
                'payload': payload,
                'status_code': None,
                'final_url': url,
                'error': repr(e),
                'content': 'Request failed'
            })
    return results
