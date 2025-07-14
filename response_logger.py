# response_logger.py
def log_summary(results):
    success_codes = [200, 301, 302, 500]
    successful = [r for r in results if r['status_code'] in success_codes]

    if successful:
        print("\n==================== ✅ BYPASS SUCCESS ====================")
        print("[✔] Bypassed Payload(s) Found:\n")
        for r in successful:
            print(f"→ Payload       : {r['payload']}")
            print(f"→ Status Code   : {r['status_code']}")
            print(f"→ Final URL     : {r['final_url']}")
            print("-----------------------------------------------------------")
    else:
        print("\n==================== ❌ WAF NOT BYPASSED ===================")
        print("Tried all payloads but none successfully bypassed the WAF.")
        print("- All requests returned 403, 404, or no significant difference.")
        print("============================================================")
