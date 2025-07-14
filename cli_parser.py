import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Active WAF Bypass Engine")
    parser.add_argument('--url', required=True, help='Target URL with FUZZ marker')
    parser.add_argument('--type', required=True, choices=['sqli', 'xss', 'lfi', 'rce'], help='Type of attack payloads')
    parser.add_argument('--p', help='Manual payload string')
    parser.add_argument('--auto', action='store_true', help='Use built-in or custom payload list')
    parser.add_argument('--w', default='./payloads', help='Path to payload directory (default: ./payloads)')
    return parser.parse_args()
