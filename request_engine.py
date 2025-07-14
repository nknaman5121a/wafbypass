import requests
import hashlib
import html
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
                post_url = base_url  # ✅ preserve query string

                data = {}
                for param in post_params:
                    key, val = param.split('=')
                    data[key] = payload if 'FUZZ' in val else val

                r = requests.post(post_url, data=data, timeout=5, allow_redirects=True)
            else:
                r = requests.get(url, timeout=5, allow_redirects=True)

            # Smart reflection & XSS detection
            decoded_payload = html.unescape(payload)

            # Basic reflection
            is_raw_reflected = payload in r.text or decoded_payload in r.text

            # False-positive sanitizer patterns (escaped HTML)
            bad_signatures = ["&lt;", "&gt;", "&#x3c;", "&#x3e;", "\\u003c", "\\u003e"]
            sanitized = any(sig in r.text for sig in bad_signatures)

            # Final result: reflected and not encoded
            is_reflected = is_raw_reflected and not sanitized

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
