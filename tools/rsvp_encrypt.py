#!/usr/bin/env python3
"""RSVP 집계 JSON을 AES-GCM으로 암호화해 party/rsvp-data.enc 로 저장.

사용법: python3 tools/rsvp_encrypt.py <base64url키> < 집계.json  (pip install pycryptodome 필요)
출력 포맷: base64( 12바이트 IV + ciphertext ) 텍스트 한 줄.
후태 페이지(party/rsvp.html)가 URL 해시의 같은 키로 복호화한다.
"""
import sys, os, json, base64
from Crypto.Cipher import AES

def b64u_decode(s):
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    key = b64u_decode(sys.argv[1])
    data = json.loads(sys.stdin.read())
    plaintext = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode()
    iv = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    out = base64.b64encode(iv + ct + tag).decode()
    path = os.path.join(os.path.dirname(__file__), '..', 'party', 'rsvp-data.enc')
    with open(path, 'w') as f:
        f.write(out)
    print(f'암호화 완료: {len(data.get("entries", []))}건 -> party/rsvp-data.enc')

if __name__ == '__main__':
    main()
