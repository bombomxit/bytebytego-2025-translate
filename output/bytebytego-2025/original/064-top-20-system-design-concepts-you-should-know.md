# 064 - Top 20 System Design Concepts You Should Know

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 134-138
- Figures: 2

## Figures

![Top 20 System Design Concepts You Should Know - figure 1](../assets/064/figure-01.png)
![Top 20 System Design Concepts You Should Know - figure 2](../assets/064/figure-02.png)

## Original Extracted Text

1. Load Balancing: Distributes traffic across multiple servers for reliability and availability.

 2. Caching: Stores frequently accessed data in memory for faster access.

 3. Database Sharding: Splits databases to handle large-scale data growth.

 4. Replication: Copies data across replicas for availability and fault tolerance.

 5. CAP Theorem: Trade-off between consistency, availability, and partition tolerance.

 6. Consistent Hashing: Distributes load evenly in dynamic server environments.

 7. Message Queues: Decouples services using asynchronous event-driven architecture.

   8. Rate Limiting: Controls request frequency to prevent system overload.

   9. API Gateway: Centralized entry point for routing API requests.

   10.Microservices: Breaks systems into independent, loosely coupled services.

   11. Service Discovery: Locates services dynamically in distributed systems.

   12.CDN: Delivers content from edge servers for speed.

   13.Database Indexing: Speeds up queries by indexing important fields.

   14.Data Partitioning: Divides data across nodes for scalability and performance.

   15.Eventual Consistency: Guarantees consistency over time in distributed databases

   16.WebSockets: Enables bi-directional communication for live updates.

   17.Scalability: Increases capacity by upgrading or adding machines.

   18.Fault Tolerance: Ensures system availability during hardware/software failures.

   19.Monitoring: Tracks metrics and logs to understand system health.

   20.Authentication & Authorization: Controls user access and verifies identity securely.

Over to you: Which other System Design concept will you add to the list?

Essential Git Cheatsheet!

🔧 Basic Commands
git init - Initialize a new Git repository.

git clone <repo_url> - Clone a remote repository.

git status - Check the status of your working directory.

git add <file> - Stage changes for commit.

git commit -m "message" - Commit staged changes with a message.

git push - Push your local commits to the remote repository.

git pull - Fetch and merge changes from the remote repo.

git diff - Show changes in the working directory (uncommitted changes).

git diff --staged - Show changes between the staging area and last commit.

🛠️ Branching & Merging
git branch - List branches.

git branch <branch_name> - Create a new branch.

git checkout <branch_name> - Switch to another branch.

git checkout -b <branch_name> - Create and switch to a new branch.

git merge <branch_name> - Merge a branch into the current one.

git branch -d <branch_name> - Delete a branch after merging.

git branch -D <branch_name> - Forcefully delete a branch, even if it hasn't merged.

🔄 Synchronization
git fetch - Download changes from remote without merging.

git rebase <branch> - Reapply commits on top of another branch to maintain linear history.

git pull --rebase - Fetch and reapply your changes on top of the latest remote changes.

git remote add <name> <url> - Add a new remote repository.

🎯 Advanced Git
git stash - Temporarily save changes without committing.

git stash pop - Reapply stashed changes.

git cherry-pick <commit> - Apply a specific commit to your current branch.

git log --oneline - View simplified commit history.

git reflog - Show the history of your reference changes (e.g., checkout, resets).

git log --graph --decorate --all - Show a visual commit history.

🚨 Undoing Changes
git reset <file> - Unstage a file.

git reset --soft <commit> - Reset to a commit but keep changes in the working directory.

git reset --hard <commit> - Completely reset to a previous commit, discarding changes.

git revert <commit> - Create a new commit that undoes a specific commit.

⚙️ Collaborating with Others
git fork - Fork a repository on GitHub (via UI) to start contributing.

git pull origin <branch> - Pull changes from the original remote branch.

git push origin <branch> - Push your branch to the original repository for collaboration.

Over to you: did we miss anything?
