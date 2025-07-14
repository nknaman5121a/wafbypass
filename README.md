# 🔥 WAF Bypass Engine (CLI Tool)

A powerful command-line tool to **automatically mutate payloads and test WAF bypass techniques** for SQLi, XSS, LFI, and RCE.

---

## 🚀 Features

- 🎯 Supports: `SQLi`, `XSS`, `LFI`, `RCE`
- 🔁 Payload mutation engine (encoding, obfuscation, polyglots, wrappers)
- 🧪 Sends requests and analyzes responses
- 🖥️ Terminal-based success logger (no file storage)
- 📦 Supports auto-payloads or custom ones

---

## 🔧 Installation

### 📦 Requirements
- Python **3.7+**
- `requests` library

### ✅ Steps to Install

```bash
# Clone the repository
git clone https://github.com/nknaman5121a/wafbypass.git
cd wafbypass

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install requests
```

Then run it like:

```bash
python wafbypass.py --url "https://example.com/search?q=FUZZ" --type xss --auto
```

---

## 🧾 Usage

```bash
python wafbypass.py --url "https://example.com/search.php?q=FUZZ" --type sqli --auto
```

---

## ⚙️ Flags

| Flag        | Description                                                  |
|-------------|--------------------------------------------------------------|
| `--url`     | **(Required)** Target URL with `FUZZ` marker                 |
| `--type`    | **(Required)** Payload type: `sqli`, `xss`, `lfi`, or `rce`  |
| `--p`       | Provide a single manual payload                              |
| `--auto`    | Use auto payloads from `payloads/` folder                    |
| `--w`       | Custom path to payload directory (default: `./payloads`)     |

---

## 💡 Examples

### Auto test SQLi with built-in payloads:
```bash
python wafbypass.py --url "https://target.com/item?id=FUZZ" --type sqli --auto
```

### Custom XSS payload test:
```bash
python wafbypass.py --url "https://target.com/search?q=FUZZ" --type xss --p "<svg/onload=alert(1)>"
```

### Use custom payload directory:
```bash
python wafbypass.py --url "https://target.com/vuln=FUZZ" --type rce --auto --w ./custom_payloads
```

---

## 📁 Payload Folder Structure

```
payloads/
├── sqli.txt
├── xss.txt
├── lfi.txt
└── rce.txt
```

- Each file contains one payload per line.
- These are mutated before being sent in requests.

---

## ✅ Example Output

```bash
==================== ✅ BYPASS SUCCESS ====================
[✔] Bypassed Payload(s) Found:

→ Payload       : %2527%20OR%201%3D1%20--
→ Status Code   : 200
→ Final URL     : https://example.com/search.php?q=%2527%20OR%201%3D1%20--

→ Payload       : <svg onload=alert(1)>
→ Status Code   : 302
→ Final URL     : https://example.com/search.php?q=<svg...>
→ Redirected To : /admin/dashboard
```

Or if no payloads succeeded:

```bash
==================== ❌ WAF NOT BYPASSED ===================
Tried all payloads but none successfully bypassed the WAF.
============================================================
```

---

## 🧠 Mutation Techniques Used

- URL encoding / double encoding
- Unicode / Base64 / Hex
- SQL keyword splitting (`UN/**/ION`)
- Polyglot XSS payloads
- LFI with wrappers (`php://filter`)
- RCE tricks (`${IFS}`, `$(...)`)

---

## 👤 Author

- **Name**: Naman Kumar ([@nknaman5121a](https://github.com/nknaman5121a))
- **Focus**: Offensive Security, WAF bypass, and automation

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes and authorized penetration testing** only.  
Using it against systems without permission is illegal and unethical.

---
