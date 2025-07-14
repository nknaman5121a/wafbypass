# response_logger.py

def log_summary(results):
    success_codes = [200, 301, 302, 500]

    # ✅ Use .get() to avoid KeyError
    successful = [r for r in results if r.get('status_code') in success_codes]

    if successful:
        print("\n==================== ✅ BYPASS SUCCESS ====================")
        print("[✔] Bypassed Payload(s) Found:\n")
        for r in successful:
            print(f"→ Payload       : {r.get('payload')}")
            print(f"→ Status Code   : {r.get('status_code')}")
            print(f"→ Final URL     : {r.get('final_url')}")
            print("-----------------------------------------------------------")
    else:
        print("\n==================== ❌ WAF NOT BYPASSED ===================")
        print("Tried all payloads but none successfully bypassed the WAF.")
        print("- All requests returned 403, 404, or no significant difference.")
        print("============================================================")

    # ✅ Optional: Log errors or failed requests
    #failed = [r for r in results if r.get('status_code') is None]
    #if failed:
     #   print("\n[!] Errors encountered during request:")
      #  for r in failed:
       #     print(f"→ Payload: {r.get('payload')}")
        #    print(f"→ Error  : {r.get('content')}")
         #   print("-----------------------------------------------------------")
