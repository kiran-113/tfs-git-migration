
# TFS → Azure Repos Migration Tool

This Python script automates the migration of repositories from **TFS (Team Foundation Server)** to **Azure Repos (Git)** using [git-tfs](https://github.com/git-tfs/git-tfs).
It handles prerequisites, cloning, branch mapping, and pushing branches to the destination repository.

---

## 🚀 Features
- **Prerequisite checks**: Ensures `Git` and `git-tfs` are installed.
- **Interactive setup**: Prompts for clone directory, TFS details, and destination repo.
- **Progress streaming**: Displays real-time progress during TFS clone.
- **Branch mapping**: Explains how TFS root branch maps to Git `master`.
- **Flexible push options**: Push all branches or a limited number.
- **Summary report**: Lists successful and failed branch pushes.

---

## 📋 Prerequisites
- Python 3.x
- Git installed (`git --version`)
- git-tfs installed (`git tfs --version`) → [Download git-tfs](https://github.com/git-tfs/git-tfs)
- Access to both:
  - TFS Collection URL
  - Azure DevOps Git repository URL

---

## ⚙️ Usage

1. Clone or download this repository.
2. Run the script:
   ```bash
   python migrate_tfs_to_azure.py
   ```
3. Follow the prompts:
   - Enter **clone directory** (e.g., `D:\tfs-migration\demo123`)
   - Enter **TFS Collection URL** (e.g., `http://server:8080/tfs/TeamProject`)
   - Enter **TFS Root branch path (here `$` is Mandatory)** (e.g., `$/demo123/test`)
   - Choose whether to push **all branches** or only the first **N branches**
   - Enter **destination Azure Repo URL (Works with any Reops)** (e.g., `https://user@dev.azure.com/org/project/_git/repo`)

---

## 🔄 Workflow Overview

```text
+-------------------+        +-------------------+        +-------------------+
|   TFS Repository  | -----> |   git-tfs Clone   | -----> |   Local Git Repo  |
+-------------------+        +-------------------+        +-------------------+
                                                           |
                                                           v
                                                +---------------------------+
                                                |   Azure or Any  Repos     |
                                                +---------------------------+
```

**Step-by-step flow:**
1. **Check prerequisites** → Git and git-tfs must be installed.
2. **Clone TFS repo** → Using `git tfs clone` with all branches.
3. **Map branches** → TFS root branch → Git `master`.
4. **Configure remote** → Add Azure Repo as `origin`.
5. **Push branches** → All or selected branches pushed to Azure Repos.
6. **Summary report** → Shows success/failure for each branch.

---

## 📦 Example Workflow

```text
==============================
 TFS → Azure Repos Migration
==============================

🔍 Checking prerequisites...
✅ Git is installed
✅ git-tfs is installed

📁 Clone Location
Enter directory path where TFS repo should be cloned
(example: D:\tfs-migration\demo123):

📥 TFS Repository Details
Enter TFS Collection URL:
Enter TFS ROOT branch path:

📦 Cloning TFS repository with all branches...
⏳ This may take time. Progress will be shown below.

ℹ️ IMPORTANT NOTE
The TFS root branch you provided:
  $/demo123/test
is automatically migrated to the Git branch:
  master
```

---

## 📂 Output
- Cloned repository with all branches.
- Remote `origin` configured to destination Azure Repo.
- Branches pushed with success/failure summary.

---

## ✅ Migration Summary Example

```text
==============================
 Migration Summary
==============================

✅ Successful branches (3):
  - master
  - feature/login
  - feature/dashboard

🎉 No failures!
```

---

## ⚠️ Notes
- The **TFS root branch** always maps to Git `master` (default `git-tfs` behavior).
- Ensure the **destination repo** is empty or ready to accept pushes.
- Large repositories may take significant time to clone and push.

---

## 📜 License
This script is provided as-is for internal migration purposes.
Modify and adapt as needed for your environment.
```
