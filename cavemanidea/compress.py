#!/usr/bin/env python3
"""
Caveman Memory Compression Orchestrator for LM Studio
Usage:
    python compress.py <filepath>
"""

import re
import sys
from pathlib import Path
from typing import List

from openai import OpenAI

BASE_URL = "address of llm/avaliable at(local server)"
MODEL_NAME = "Name of llm"
OUTPUT_DIR = Path("compressed")
MAX_FILE_SIZE = 500_000

client = OpenAI(base_url=BASE_URL, api_key="not-needed")

OUTER_FENCE_REGEX = re.compile(r"\A\s*(`{3,}|~{3,})[^\n]*\n(.*)\n\1\s*\Z", re.DOTALL)
SENSITIVE_BASENAME_REGEX = re.compile(
    r"(?ix)^(" 
    r"\.env(\..+)?"
    r"|\.netrc"
    r"|credentials(\..+)?"
    r"|secrets?(\..+)?"
    r"|passwords?(\..+)?"
    r"|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?"
    r"|authorized_keys"
    r"|known_hosts"
    r"|.*\.(pem|key|p12|pfx|crt|cer|jks|keystore|asc|gpg)"
    r")$"
)
SENSITIVE_PATH_COMPONENTS = frozenset({".ssh", ".aws", ".gnupg", ".kube", ".docker"})
SENSITIVE_NAME_TOKENS = (
    "secret", "credential", "password", "passwd",
    "apikey", "accesskey", "token", "privatekey",
)


def is_sensitive_path(filepath: Path) -> bool:
    name = filepath.name
    if SENSITIVE_BASENAME_REGEX.match(name):
        return True
    lowered_parts = {p.lower() for p in filepath.parts}
    if lowered_parts & SENSITIVE_PATH_COMPONENTS:
        return True
    lower = re.sub(r"[_\-\s.]", "", name.lower())
    return any(tok in lower for tok in SENSITIVE_NAME_TOKENS)


def strip_llm_wrapper(text: str) -> str:
    m = OUTER_FENCE_REGEX.match(text)
    return m.group(2) if m else text


def build_compress_prompt(original: str) -> str:
    return f"""
Rewrite this markdown in short caveman style.
Keep technical meaning exact.
Keep code blocks, inline code, URLs, and headings unchanged.
Remove filler words and make prose shorter.
Return plain markdown only.

TEXT:
{original}
"""


def call_local_model(prompt: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You shorten markdown text. Keep technical meaning exact. Return plain markdown only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2000,
    )

    if not getattr(resp, "choices", None):
        raise RuntimeError(f"No choices returned: {resp}")

    msg = resp.choices[0].message
    if not msg or msg.content is None:
        raise RuntimeError(f"Empty message content: {resp}")

    return strip_llm_wrapper(msg.content.strip())


def compress_file(filepath: Path) -> bool:
    filepath = filepath.resolve()

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath.stat().st_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large to compress safely (max 500KB): {filepath}")
    if is_sensitive_path(filepath):
        raise ValueError(f"Refusing to compress sensitive-looking file: {filepath}")

    print(f"Processing: {filepath}")
    original_text = filepath.read_text(encoding="utf-8", errors="ignore")
    compressed = call_local_model(build_compress_prompt(original_text))

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / filepath.name
    backup_path = filepath.with_suffix(filepath.suffix + ".original")

    backup_path.write_text(original_text, encoding="utf-8")
    out_path.write_text(compressed, encoding="utf-8")

    print(f"Backup saved: {backup_path}")
    print(f"Compressed saved: {out_path}")
    print(f"Original chars: {len(original_text):,}")
    print(f"Compressed chars: {len(compressed):,}")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress.py <filepath>")
        sys.exit(1)

    compress_file(Path(sys.argv[1]))
