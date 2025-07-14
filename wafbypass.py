### wafbypass.py (entry point)
from cli_parser import parse_args
from payload_loader import PayloadLoader
from payload_mutator import mutate_payloads
from request_engine import send_requests
from response_logger import log_summary

def main():
    args = parse_args()

    print("[+] Loading payloads...")
    loader = PayloadLoader(
        payload_type=args.type,
        single_payload=args.p,
        auto_payloads=args.auto,
        payloads_path=args.w
    )

    payloads = loader.load_payloads()

    if not payloads:
        print("[!] No payloads found. Exiting.")
        return

    print(f"[+] Loaded {len(payloads)} payload(s)")

    mutated_payloads = mutate_payloads(payloads, args.type)
    print(f"[+] Generated {len(mutated_payloads)} mutated payload(s)")

    results = send_requests(args.url, mutated_payloads)

    log_summary(results)

if __name__ == "__main__":
    main()
