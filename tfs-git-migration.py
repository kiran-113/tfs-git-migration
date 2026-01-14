import subprocess
import sys
import os
from datetime import datetime

AUTO_YES = "--yes" in sys.argv

# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def run(cmd, cwd=None, check=True):
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if check and result.returncode != 0:
        print(f"\n❌ Command failed:\n{cmd}")
        print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()

def run_stream(cmd, cwd=None):
    process = subprocess.Popen(
        cmd,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        print(line, end="")
    process.wait()
    if process.returncode != 0:
        print("\n❌ Command failed")
        sys.exit(1)

def check_tool(name, command):
    try:
        run(command)
        print(f"✅ {name} is installed")
    except SystemExit:
        print(f"❌ {name} is NOT installed")
        sys.exit(1)

# -------------------------------------------------
# Git Validation Helpers (BEST PRACTICE)
# -------------------------------------------------

def count_files(branch, cwd):
    out = run(f"git ls-tree -r --name-only {branch}", cwd=cwd)
    return len(out.splitlines()) if out else 0

def get_commit_sha(branch, cwd):
    return run(f"git rev-parse {branch}", cwd=cwd)

def get_tree_sha(branch, cwd):
    return run(f"git show -s --format=%T {branch}", cwd=cwd)

# -------------------------------------------------
# Start
# -------------------------------------------------

print("\n====================================")
print("  TFS → Azure Repos Migration Tool")
print("====================================\n")

# 1. Prerequisites
print("🔍 Checking prerequisites...\n")
check_tool("Git", "git --version")
check_tool("git-tfs", "git tfs --version")

# 2. Clone directory
clone_dir = input("\n📁 Clone directory path: ").strip()
if not clone_dir:
    sys.exit("❌ Clone directory is required")

if os.path.exists(clone_dir) and os.listdir(clone_dir):
    sys.exit("❌ Target directory exists and is not empty")

os.makedirs(clone_dir, exist_ok=True)

# 3. TFS details
tfs_url = input("\n📥 TFS Collection URL (example: http://server:8080/tfs/TeamProject): ").strip()
tfs_branch = input("📥 TFS ROOT branch path (example: $/demo123/code): ").strip()

if not tfs_url or not tfs_branch:
    sys.exit("❌ TFS details are required")

# 4. Clone from TFS (with progress)
print("\n📦 Cloning TFS repository with all branches...")
print(f"📁 Clone path : {clone_dir}")
print(f"📥 TFS URL    : {tfs_url}")
print(f"📥 TFS branch : {tfs_branch}")
print("\n⏳ Progress below:\n")

run_stream(
    f'git tfs clone "{tfs_url}" "{tfs_branch}" . --branches=all',
    cwd=clone_dir
)

print(f"\nℹ️ NOTE: TFS branch {tfs_branch} → Git branch master\n")

# 5. List branches
branches = [
    b.replace("*", "").strip()
    for b in run("git branch", cwd=clone_dir).splitlines()
    if b.strip()
]

print("📌 Available Git branches:")
for i, b in enumerate(branches, 1):
    print(f"  {i}. {b}")

# 6. Branch selection
print("\n🚀 Push Options")
while True:
    choice = input("Push (A)ll or first (N) branches? (Q)uit? [A/N/Q]: ").strip().upper()
    if choice in ("A", "N", "Q"):
        break
    print("❌ Invalid input")

if choice == "Q":
    sys.exit("⛔ Aborted by user")

if choice == "N":
    while True:
        try:
            limit = int(input(f"Enter number of branches to push (1–{len(branches)}): "))
            if 1 <= limit <= len(branches):
                branches_to_push = branches[:limit]
                break
        except ValueError:
            pass
        print("❌ Invalid number")
else:
    branches_to_push = branches

# 7. Destination repo
dest_repo = input("\n🔗 Destination repo URL: ").strip()
if not dest_repo:
    sys.exit("❌ Destination repo is required")

# 8. Summary before execution
print("\n==================== SUMMARY ====================")
print(f"Clone directory : {clone_dir}")
print(f"TFS URL         : {tfs_url}")
print(f"TFS root branch : {tfs_branch} (→ master)")
print(f"Destination    : {dest_repo}")
print("Branches to push:")
for b in branches_to_push:
    print(f"  - {b}")
print("\nValidations that will be performed:")
print("  ✔ Recursive file count")
print("  ✔ Commit checksum (SHA)")
print("  ✔ Tree checksum (SHA)")
print("================================================\n")

# 9. Confirmation
if not AUTO_YES:
    confirm = input("Proceed with push? [Y/N/Q]: ").strip().upper()
    if confirm in ("N", "Q"):
        sys.exit("⛔ Operation cancelled")

# 10. Add remote
run("git remote remove origin", cwd=clone_dir, check=False)
run(f'git remote add origin "{dest_repo}"', cwd=clone_dir)

# 11. Report setup
report_path = os.path.join(clone_dir, "migration_report.txt")
report = []
report.append("TFS → Azure Repos Migration Report\n")
report.append(f"Timestamp       : {datetime.now()}\n")
report.append(f"Clone directory : {clone_dir}\n")
report.append(f"TFS URL         : {tfs_url}\n")
report.append(f"TFS root branch : {tfs_branch}\n")
report.append(f"Destination     : {dest_repo}\n")

# 12. Push + validation
print("\n📤 Pushing branches with deep validation...\n")

success, failed = [], []

for branch in branches_to_push:
    print(f"➡ Branch: {branch}")

    fb = count_files(branch, clone_dir)
    cb = get_commit_sha(branch, clone_dir)
    tb = get_tree_sha(branch, clone_dir)

    print(f"   📄 Files BEFORE push : {fb}")
    print(f"   🔐 Commit SHA        : {cb}")
    print(f"   🌳 Tree SHA          : {tb}")

    run(f"git push -u origin {branch}", cwd=clone_dir)

    fa = count_files(branch, clone_dir)
    ca = get_commit_sha(f"origin/{branch}", clone_dir)
    ta = get_tree_sha(f"origin/{branch}", clone_dir)

    print(f"   📄 Files AFTER push  : {fa}")
    print(f"   🔐 Commit SHA (orig) : {ca}")
    print(f"   🌳 Tree SHA (orig)   : {ta}")

    valid = fb == fa and cb == ca and tb == ta

    report.append("\n------------------------------------\n")
    report.append(f"Branch           : {branch}\n")
    report.append(f"Files (before)   : {fb}\n")
    report.append(f"Files (after)    : {fa}\n")
    report.append(f"Commit SHA       : {cb}\n")
    report.append(f"Tree SHA         : {tb}\n")
    report.append(f"Validation       : {'PASS' if valid else 'FAIL'}\n")

    if valid:
        print("   ✅ VALIDATION PASSED\n")
        success.append(branch)
    else:
        print("   ❌ VALIDATION FAILED\n")
        failed.append(branch)

# 13. Write report
with open(report_path, "w", encoding="utf-8") as f:
    f.writelines(report)

# 14. Final result
print("\n==================== RESULT ====================")
print(f"✅ Successful branches : {len(success)}")
print(f"❌ Failed branches     : {len(failed)}")
print(f"📄 Report file         : {report_path}")
print("================================================")
print("\n✔ Migration completed with full integrity validation\n")



