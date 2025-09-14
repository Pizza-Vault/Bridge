import os, json, subprocess, requests

repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_REF", "").split("/")[-1]
token = os.getenv("GITHUB_TOKEN")

# Diff der PR-Änderungen holen
diff = subprocess.check_output(["git", "diff", "HEAD^..HEAD", "--unified=0"], text=True)

# OpenAI-Aufruf (modelliere generisch – trage dein Modell ein)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = "gpt-4o-mini"  # oder dein bevorzugtes Modell

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Du bist ein strenger Code-Reviewer. Präzise, kurz, mit konkreten Code-Snippets/Unified-Diff-Vorschlägen."},
            {"role": "user", "content": f"Reviewe diesen Git-Diff und schlage konkrete Patches vor:\n\n{diff}\n\nFormatiere Fixes als Unified-Diff, sonst als Aufzählung."}
        ],
        "temperature": 0.1
    },
    timeout=120
)
out = resp.json()
text = out["choices"][0]["message"]["content"]

# Kommentar in die PR posten
api = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
requests.post(
    api,
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    json={"body": text},
    timeout=60
)
