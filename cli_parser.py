import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Active WAF Bypass Engine")
    parser.add_argument('--url', required=True, help='Target URL with FUZZ marker')
    parser.add_argument('--type', required=True, choices=['sqli', 'xss', 'lfi', 'rce'], help='Type of attack payloads')
    parser.add_argument('--p', help='Manual payload string')
    parser.add_argument('--auto', action='store_true', help='Use built-in or custom payload list')
    parser.add_argument('--w', default='./payloads', help='Path to payload directory (default: ./payloads)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output (payloads sent, errors, etc.)')
    parser.add_argument('--method', default='GET', choices=['GET', 'POST'], help='HTTP method to use (default: GET)')
    parser.add_argument('--params', nargs='+', help='POST parameters as key=FUZZ or key=value (FUZZ is required in at least one)')
    return parser.parse_args()
