import requests
import hashlib
from urllib.parse import urlparse, parse_qs

def send_requests(base_url, payloads, verbose=False, method="GET", post_params=None):
    results = []

    # Prepare baseline
    try:
        baseline_response = requests.get(base_url.replace("FUZZ", "baseline"), timeout=5)
        baseline_text = baseline_response.text
    except Exception as e:
        baseline_text = ""
        if verbose:
            print(f"[!] Failed to get baseline response: {repr(e)}")

    for payload in payloads:
        url = base_url.replace("FUZZ", payload)
        if verbose:
            print(f"[>] Sending payload: {payload}")

        try:
            if method.upper() == "POST" and post_params:
                post_url = base_url  # ✅ fix: preserve query string

                data = {}
                for param in post_params:
                    if 'FUZZ' in param:
                        key, val = param.split('=')
                        data[key] = payload
                    else:
                        key, val = param.split('=')
                        data[key] = val

                r = requests.post(post_url, data=data, timeout=5, allow_redirects=True)
            else:
                r = requests.get(url, timeout=5, allow_redirects=True)

            is_reflected = payload in r.text
            is_diff = r.text != baseline_text

            results.append({
                'payload': payload,
                'status_code': r.status_code,
                'hash': hashlib.md5(r.text.encode()).hexdigest(),
                'length': len(r.text),
                'final_url': r.url,
                'location': r.headers.get('Location'),
                'content': r.text[:300],
                'reflected': is_reflected,
                'differs': is_diff
            })

        except Exception as e:
            if verbose:
                print(f"[!] Error sending request for payload: {payload}\n    └─ {repr(e)}")
            results.append({
                'payload': payload,
                'status_code': None,
                'final_url': url,
                'error': repr(e),
                'content': 'Request failed',
                'reflected': False,
                'differs': False
            })

    return results
