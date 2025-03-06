# **GitHub CLI: The Ultimate Guide for Developers' Productivity**  

GitHub CLI (`gh`) is a powerful command-line tool that helps developers interact with GitHub directly from the terminal, reducing context switching and boosting productivity. With `gh`, you can manage repositories, pull requests, issues, workflows, and more—without ever leaving your terminal.

---
### **Authenticate with GitHub**  
After installation, log in to your GitHub account:  
```sh
gh auth login
```
It will prompt you to select authentication via a browser or token. For full API access, choose `HTTPS` and authenticate with GitHub.

---

## **2. Repository Management**
### **Create a Repository**
Create a new GitHub repository without leaving your terminal:
```sh
gh repo create my-repo --public
```
or initialize it locally and push:
```sh
gh repo create my-repo --private --source=. --push
```

### **Clone a Repository**
Instead of `git clone`, use:
```sh
gh repo clone owner/repository
```
This is faster and automatically sets up authentication.

### **Fork a Repository**
```sh
gh repo fork owner/repo-name --clone
```
This clones the forked repo instantly.

---

## **3. Managing Issues**
### **Create an Issue**
```sh
gh issue create --title "Bug in authentication" --body "Steps to reproduce..."
```
To assign a user and label:
```sh
gh issue create --title "Bug in login" --assignee username --label bug
```

### **List and Filter Issues**
```sh
gh issue list --label "bug" --assignee "@me"
```
Get detailed issue view:
```sh
gh issue view 23  # View issue with ID 23
```

### **Close an Issue**
```sh
gh issue close 23
```

---

## **4. Working with Pull Requests (PRs)**
### **Create a Pull Request**
```sh
gh pr create --base main --head feature-branch --title "New Feature" --body "Description"
```

### **List Pull Requests**
```sh
gh pr list --assignee "@me"
```

### **Review & Merge PR**
- **View PR Details**  
  ```sh
  gh pr view 12
  ```
- **Approve a PR**  
  ```sh
  gh pr review 12 --approve
  ```
- **Merge PR**  
  ```sh
  gh pr merge 12 --squash --delete-branch
  ```
  
---

## **5. Automating Workflows**
### **Trigger GitHub Actions**
If your repository has GitHub Actions set up:
```sh
gh workflow list
gh workflow run deploy.yml
```

### **View Workflow Status**
```sh
gh run list
gh run view 12345  # View details of a specific run
```

---

## **6. Tips & Tricks for Maximum Productivity**
### **Enable Aliases for Shortcuts**
Avoid typing long commands:
```sh
gh alias set cpr 'pr create --fill'
gh alias set ci 'issue create --title'
```
Now, just run:
```sh
gh cpr
gh ci "Bug report"
```

### **Use TUI (Text UI) for Interactive Mode**
Instead of listing PRs manually, use interactive mode:
```sh
gh pr list --web
```
This opens the PRs in a web view.

### **Quickly Open Repos in Browser**
```sh
gh repo view --web
```

### **Check Notifications & Mentions**
```sh
gh notifications
```

### **Batch Resolve Issues with a Single Command**
If you manage multiple issues, batch-close them:
```sh
gh issue list --label "duplicate" | awk '{print $1}' | xargs -I {} gh issue close {}
```
## 7. **Some Bonus Tips**
### Search & Open a GitHub Repository in Browser
Use this one-liner to search repositories inside an organization and open the selected one in your browser:
```sh
gh search repos --owner org-name --limit 10 | fzf | awk '{print $1}' | xargs gh repo view --web
```

**Explanation:**
	•	gh search repos --owner org-name --limit 10 → Lists 10 repositories from the specified organization.
	•	fzf → Provides an interactive list to choose from.
	•	awk '{print $1}' → Extracts the repository name.
	•	xargs gh repo view --web → Opens the selected repository in your browser.


You can also create a alias for this command, add below line in your shell configuration file (~/.bashrc, ~/.zshrc, or ~/bash_aliases):
```sh
alias ghsearch="gh search repos --owner org-name --limit 10 | fzf | awk '{print \$1}' | xargs gh repo view --web"
```
```
---Conclusion

## **Conclusion**
GitHub CLI is an essential tool for developers looking to streamline their workflow. By integrating it into your daily tasks, you can save time, automate repetitive tasks, and work more efficiently.  

Would you like an infographic summarizing these commands? 🚀
