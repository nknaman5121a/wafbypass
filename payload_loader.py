import os

class PayloadLoader:
    def __init__(self, payload_type, single_payload=None, auto_payloads=False, payloads_path='./payloads'):
        self.payload_type = payload_type
        self.single_payload = single_payload
        self.auto_payloads = auto_payloads
        self.payloads_path = payloads_path

    def load_payloads(self):
        if self.single_payload:
            return [self.single_payload.strip()]

        if self.auto_payloads:
            file_path = os.path.join(self.payloads_path, f"{self.payload_type}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f if line.strip()]
            else:
                print(f"[!] Payload file not found: {file_path}")

        return []
