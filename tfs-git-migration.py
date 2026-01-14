#tfs-git-migration
import subprocess
import sys
import os

# -----------------------------
# Utility Functions
# -----------------------------

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
        print(f"➡ Please install {name} and re-run this tool")
        sys.exit(1)

# -----------------------------
# Start
# -----------------------------

print("\n==============================")
print(" TFS → Azure Repos Migration ")
print("==============================\n")

# 1. Check prerequisites
print("🔍 Checking prerequisites...\n")
check_tool("Git", "git --version")
check_tool("git-tfs", "git tfs --version")

# 2. Ask clone directory
print("\n📁 Clone Location\n")
clone_dir = input(
    "Enter directory path where TFS repo should be cloned\n"
    "(example: D:\\tfs-migration\\demo123): "
).strip()

if not clone_dir:
    print("❌ Clone directory is required")
    sys.exit(1)

if os.path.exists(clone_dir) and os.listdir(clone_dir):
    print("❌ Target directory exists and is not empty")
    sys.exit(1)

os.makedirs(clone_dir, exist_ok=True)

# 3. Ask TFS details
print("\n📥 TFS Repository Details\n")

tfs_url = input(
    "Enter TFS Collection URL\n"
    "(example: http://server:8080/tfs/TeamProject): "
).strip()

tfs_branch = input(
    "Enter TFS ROOT branch path\n"
    "(example: $/demo123/test): "
).strip()

if not tfs_url or not tfs_branch:
    print("❌ TFS URL and branch path are required")
    sys.exit(1)

# 4. Clone from TFS (WITH PROGRESS)
print("\n📦 Cloning TFS repository with all branches...")
print("⏳ This may take time. Progress will be shown below.\n")

run_stream(
    f'git tfs clone "{tfs_url}" "{tfs_branch}" . --branches=all',
    cwd=clone_dir
)

# 5. Explain master branch mapping
print("\nℹ️ IMPORTANT NOTE")
print("--------------------------------------------------")
print(
    f"The TFS root branch you provided:\n"
    f"  {tfs_branch}\n\n"
    f"is automatically migrated to the Git branch:\n"
    f"  master\n\n"
    f"This is normal git-tfs behavior."
)
print("--------------------------------------------------\n")

# 6. List branches
print("📂 Fetching local Git branches...\n")

branches_output = run("git branch", cwd=clone_dir)
branches = [
    b.replace("*", "").strip()
    for b in branches_output.splitlines()
    if b.strip()
]

if not branches:
    print("❌ No branches found after clone")
    sys.exit(1)

print("📌 Available branches:")
for idx, branch in enumerate(branches, start=1):
    print(f"  {idx}. {branch}")

# 7. Ask how many branches to push
print("\n🚀 Push Options\n")
choice = input(
    "Push (A)ll branches or first (N) branches? [A/N]: "
).strip().upper()

if choice == "N":
    try:
        limit = int(input(f"Enter number of branches to push(Range) (1–{len(branches)}): "))
        if limit < 1 or limit > len(branches):
            raise ValueError
        branches_to_push = branches[:limit]
    except ValueError:
        print("❌ Invalid number")
        sys.exit(1)
else:
    branches_to_push = branches

# 8. Ask destination repo
print("\n🔗 Destination Repository\n")

dest_repo = input(
    "Enter destination Git repo URL\n"
    "(example: https://user@dev.azure.com/org/project/_git/repo): "
).strip()

if not dest_repo:
    print("❌ Destination repo URL is required")
    sys.exit(1)

# 9. Add remote
print("\n🔧 Configuring remote 'origin'...\n")
run("git remote remove origin", cwd=clone_dir, check=False)
run(f'git remote add origin "{dest_repo}"', cwd=clone_dir)

# 10. Push branches
print("\n📤 Pushing branches...\n")

success = []
failed = []

for branch in branches_to_push:
    print(f"➡ Pushing branch: {branch}")
    try:
        run(f"git push -u origin {branch}", cwd=clone_dir)
        print(f"✅ Successfully pushed: {branch}\n")
        success.append(branch)
    except SystemExit:
        print(f"❌ Failed to push: {branch}\n")
        failed.append(branch)

# 11. Summary
print("\n==============================")
print(" Migration Summary")
print("==============================")

print(f"\n✅ Successful branches ({len(success)}):")
for b in success:
    print(f"  - {b}")

if failed:
    print(f"\n❌ Failed branches ({len(failed)}):")
    for b in failed:
        print(f"  - {b}")
else:
    print("\n🎉 No failures!")

print("\n✔ Migration process completed\n")


# import subprocess
# import sys
# import os

# # -----------------------------
# # Utility Functions
# # -----------------------------

# def run(cmd, cwd=None, check=True):
#     result = subprocess.run(
#         cmd,
#         shell=True,
#         cwd=cwd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     if check and result.returncode != 0:
#         print(f"\n❌ Command failed:\n{cmd}")
#         print(result.stderr.strip())
#         sys.exit(1)
#     return result.stdout.strip()

# def check_tool(name, command):
#     try:
#         run(command)
#         print(f"✅ {name} is installed")
#     except SystemExit:
#         print(f"❌ {name} is NOT installed")
#         print(f"➡ Please install {name} and re-run this tool")
#         sys.exit(1)

# # -----------------------------
# # Start
# # -----------------------------

# print("\n==============================")
# print(" TFS → Azure Repos Migration ")
# print("==============================\n")

# # 1. Check prerequisites
# print("🔍 Checking prerequisites...\n")
# check_tool("Git", "git --version")
# check_tool("git-tfs", "git tfs --version")

# # 2. Ask clone directory
# print("\n📁 Clone Location\n")
# clone_dir = input(
#     "Enter directory path where TFS repo should be cloned\n"
#     "(example: D:\\tfs-migration\\demo123): "
# ).strip()

# if not clone_dir:
#     print("❌ Clone directory is required")
#     sys.exit(1)

# if os.path.exists(clone_dir) and os.listdir(clone_dir):
#     print("❌ Target directory exists and is not empty")
#     sys.exit(1)

# os.makedirs(clone_dir, exist_ok=True)

# # 3. Ask TFS details
# print("\n📥 TFS Repository Details\n")

# tfs_url = input(
#     "Enter TFS Collection URL\n"
#     "(example: http://server:8080/tfs/TeamProject): "
# ).strip()

# tfs_branch = input(
#     "Enter TFS root branch path\n"
#     "(example: $/demo123/test): "
# ).strip()

# if not tfs_url or not tfs_branch:
#     print("❌ TFS URL and branch path are required")
#     sys.exit(1)

# # 4. Clone from TFS
# print("\n📦 Cloning TFS repository with all branches...\n")

# run(
#     f'git tfs clone "{tfs_url}" "{tfs_branch}" . --branches=all',
#     cwd=clone_dir
# )

# # 5. List branches
# print("\n📂 Fetching local Git branches...\n")

# branches_output = run("git branch", cwd=clone_dir)
# branches = [
#     b.replace("*", "").strip()
#     for b in branches_output.splitlines()
#     if b.strip()
# ]

# if not branches:
#     print("❌ No branches found after clone")
#     sys.exit(1)

# print("📌 Available branches:")
# for idx, branch in enumerate(branches, start=1):
#     print(f"  {idx}. {branch}")

# # 6. Ask how many branches to push
# print("\n🚀 Push Options\n")
# choice = input(
#     "Push (A)ll branches or first (N) branches? [A/N]: "
# ).strip().upper()

# if choice == "N":
#     try:
#         limit = int(input(f"Enter number of branches to push (1–{len(branches)}): "))
#         if limit < 1 or limit > len(branches):
#             raise ValueError
#         branches_to_push = branches[:limit]
#     except ValueError:
#         print("❌ Invalid number")
#         sys.exit(1)
# else:
#     branches_to_push = branches

# # 7. Ask destination repo
# print("\n🔗 Destination Repository\n")

# dest_repo = input(
#     "Enter destination Git repo URL\n"
#     "(example: https://user@dev.azure.com/org/project/_git/repo): "
# ).strip()

# if not dest_repo:
#     print("❌ Destination repo URL is required")
#     sys.exit(1)

# # 8. Add remote
# print("\n🔧 Configuring remote 'origin'...\n")
# run(f'git remote remove origin', cwd=clone_dir, check=False)
# run(f'git remote add origin "{dest_repo}"', cwd=clone_dir)

# # 9. Push branches
# print("\n📤 Pushing branches...\n")

# success = []
# failed = []

# for branch in branches_to_push:
#     print(f"➡ Pushing branch: {branch}")
#     try:
#         run(f"git push -u origin {branch}", cwd=clone_dir)
#         print(f"✅ Successfully pushed: {branch}\n")
#         success.append(branch)
#     except SystemExit:
#         print(f"❌ Failed to push: {branch}\n")
#         failed.append(branch)

# # 10. Summary
# print("\n==============================")
# print(" Migration Summary")
# print("==============================")

# print(f"\n✅ Successful branches ({len(success)}):")
# for b in success:
#     print(f"  - {b}")

# if failed:
#     print(f"\n❌ Failed branches ({len(failed)}):")
#     for b in failed:
#         print(f"  - {b}")
# else:
#     print("\n🎉 No failures!")

# print("\n✔ Migration process completed\n")
