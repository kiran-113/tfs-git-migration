# TFS → Azure Repos Migration Tool

This Python-based **enterprise-grade migration utility** automates the migration of repositories from
**TFS (Team Foundation Server)** to **Azure Repos (Git)** (or any Git-compatible repository) using **git-tfs**.

It is designed to be **safe, auditable, user-friendly, and EXE-ready**, with deep integrity validation to ensure **zero data loss**.

---

## 🚀 Key Capabilities

### 🔧 Prerequisites & Safety

* **Automatic prerequisite checks**

  * Verifies `Git` and `git-tfs` are installed
  * Stops execution with clear guidance if missing
* **Safe directory handling**

  * Prevents running in non-empty directories
* **Abort anytime**

  * Explicit `Q` (Quit) option before execution

---

### 📥 TFS → Git Conversion

* **Interactive TFS setup**

  * Clone directory selection
  * TFS Collection URL input
  * TFS *root branch path* input (e.g. `$/demo123/code`)
* **Live progress streaming**

  * Real-time output during `git tfs clone`
* **Automatic branch mapping**

  * Clearly informs users that:

    ```
    TFS root branch (e.g. $/demo123/code) → Git branch master
    ```

    (standard `git-tfs` behavior)

---

### 🌿 Branch Control

* Lists **all discovered Git branches**
* Allows:

  * Push **ALL branches**
  * Push **first N branches only**
* Strict input validation (no accidental pastes)

---

### 🔐 Deep Integrity Validation (Enterprise Standard)

For **each branch**, the tool validates:

| Validation               | Description                                 |
| ------------------------ | ------------------------------------------- |
| 📄 Recursive file count  | Ensures all files & folders are present     |
| 🔐 Commit checksum (SHA) | Verifies commit integrity                   |
| 🌳 Tree checksum (SHA)   | Verifies full directory structure & content |

✅ **If all three match before & after push, the migration is cryptographically guaranteed correct**

This is **stronger than filesystem hashing** and is the same validation approach used by GitHub / Azure DevOps migrations.

---

### 📋 Confirmation & Automation

* **Pre-execution summary screen**

  * Clone path
  * TFS URL & branch
  * Destination repo
  * Selected branches
  * Validation steps
* **Explicit confirmation before pushing**
* **Non-interactive mode**

  ```bash
  python tfs-git-migration.py --yes
  ```

  (Skips confirmation for automation / CI usage)

---

### 📄 Migration Report (TXT)

* Automatically generates `migration_report.txt`
* Includes:

  * Timestamp
  * Clone directory
  * TFS URL & root branch
  * Destination repo
  * Per-branch:

    * File counts (before & after)
    * Commit SHA
    * Tree SHA
    * PASS / FAIL validation status
* Suitable for **audit, compliance, and sign-off**

---

## 📋 Prerequisites

* Python **3.x**
* Git

  ```bash
  git --version
  ```
* git-tfs

  ```bash
  git tfs --version
  ```

  👉 [https://github.com/git-tfs/git-tfs](https://github.com/git-tfs/git-tfs)
* Access to:

  * TFS Collection URL
  * Destination Git repository (Azure Repos / GitHub / GitLab etc.)

---

## ⚙️ Usage

### 1️⃣ Run the script

```bash
python tfs-git-migration.py
```

(Optional non-interactive mode)

```bash
python tfs-git-migration.py --yes
```

---

### 2️⃣ Provide inputs when prompted

* **Clone directory**

  ```
  D:\tfs-migration\demo123
  ```
* **TFS Collection URL**

  ```
  http://server:8080/tfs/TeamProject
  ```
* **TFS ROOT branch path**
  ⚠️ `$` is mandatory

  ```
  $/demo123/code
  ```
* **Branch push option**

  * All branches
  * OR first N branches
* **Destination Git repo URL**

  ```
  https://user@dev.azure.com/org/project/_git/repo
  ```

---

## 🔄 Workflow Overview

```text
+-------------------+
|   TFS Repository  |
+-------------------+
          |
          v
+-------------------+
|   git-tfs Clone   |  (with progress)
+-------------------+
          |
          v
+-------------------+
|   Local Git Repo  |
|  (branches mapped)|
+-------------------+
          |
          v
+---------------------------+
|  Azure / Any Git Repos    |
| (push + deep validation)  |
+---------------------------+
```

---

## 🧪 Validation Flow (Per Branch)

```text
Before Push
 ├─ File count (recursive)
 ├─ Commit SHA
 └─ Tree SHA

Push to destination

After Push
 ├─ File count (recursive)
 ├─ Commit SHA
 └─ Tree SHA

Result
 └─ PASS only if ALL match
```

---

## 📦 Example Console Output (Simplified)

```text
➡ Branch: dev123
📄 Files BEFORE push : 12
🔐 Commit SHA        : 0f064519...
🌳 Tree SHA          : 4d53f71c...

📄 Files AFTER push  : 12
🔐 Commit SHA (orig) : 0f064519...
🌳 Tree SHA (orig)   : 4d53f71c...

✅ VALIDATION PASSED
```

---

## 📂 Output Artifacts

* Local cloned Git repository
* Destination repo populated with branches
* `migration_report.txt` (audit-ready)

---

## ⚠️ Important Notes

* **TFS root branch always maps to Git `master`**

  * This is standard `git-tfs` behavior
* Destination repository should be:

  * Empty **OR**
  * Ready to accept incoming branches
* Large repositories may take time during clone & push
* Git guarantees integrity when commit & tree SHAs match
