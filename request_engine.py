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

            response_text = r.text.lower()
            decoded_payload = html.unescape(payload).lower()

            # Step 1: Raw reflection only (no base64 or encoded junk)
            raw_reflection = payload in response_text

            # Step 2: Executable context check (real attack surface)
            exec_contexts = ["<script", "<svg", "<img", "<iframe", "onerror=", "onload=", "onclick=", "src=javascript:", "href=javascript:"]
            in_exec_context = any(ctx in response_text for ctx in exec_contexts)

            # Step 3: Avoid common encoding escapes
            bad_signatures = ["&lt;", "&gt;", "&#x3c;", "&#x3e;", "\\u003c", "\\u003e"]
            sanitized = any(sig in response_text for sig in bad_signatures)

            # Final decision
            is_reflected = raw_reflection and in_exec_context and not sanitized
            is_diff = response_text != baseline_text

            results.append({
                'payload': payload,
                'status_code': r.status_code,
                'hash': hashlib.md5(response_text.encode()).hexdigest(),
                'length': len(response_text),
                'final_url': r.url,
                'location': r.headers.get('Location'),
                'content': response_text[:300],
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
