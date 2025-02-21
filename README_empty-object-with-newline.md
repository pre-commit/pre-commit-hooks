# empty-object-with-newline check and formatter

In Shopify theme development, there is a GitHub bot which pulls in changes in GitHub repos.
Sadly it formats .json files in a non standard way. Hence, every empty object get's a newline, which doesn't not conform to standard formatting.
This creates then a new commit in the branch, which is pushed back into the origin repo. Which needs to be pulled to be able to push again. It's creating a cycle.

Hence, I created the formatting option --empty-object-with-newline to conform to the Shopify .json formatting to prevent commit pollution.

Sadly, this was not added as my pull request got declined. Hence, I kept the for up.

## Synch upstream changes

This Claude 3 Opus conversation gives the solution on how to merge in the upstream changes.

### Prompt 1

I have forked a github repo and added some commits to the main branch. Sadly, they didn't get merged with my pull request.

I would like to move the last 4 commits now in a branch, to be able to update from the upstream repo

### Response 1

Here are the steps to move your last 4 commits from the main branch to a new branch:

1. Make sure you're on the main branch:

```bash
git checkout main
```

2. Create a new branch and switch to it, e.g., named "feature-branch":

```bash
git checkout -b feature-branch
```

3. Move the main branch back by 4 commits, keeping the changes in your current branch:

```bash
git branch -f main HEAD~4
```

This effectively moves the main branch back by 4 commits, while your current branch (feature-branch) retains the commits.

4. Push the updated main branch to your forked repository (assuming your remote is named "origin"):

```bash
git push origin main --force
```

Note: Using --force is necessary because you're rewriting the history of the main branch. Make sure you're aware of the implications and that it's safe to do so.

5. Your feature-branch now contains the last 4 commits. You can push this branch to your forked repository:

```bash
git push origin feature-branch
```

After these steps, your main branch will be synchronized with the upstream repository, and your last 4 commits will be in the feature-branch.

To update your forked repository with the latest changes from the upstream repository, you can do the following:

1. Add the upstream repository as a remote (if you haven't already):

```bash
git remote add upstream <UPSTREAM_REPO_URL>
```

2. Fetch the latest changes from the upstream repository:

```bash
git fetch upstream
```

3. Merge the upstream changes into your main branch:

```bash
git checkout main
git merge upstream/main
```

4. Push the updated main branch to your forked repository:

```bash
git push origin main
```

Now your forked repository's main branch will be up to date with the upstream repository, and you can work on your feature-branch separately.

### Prompt 2

I followed the instructions,but did the update of the repo from the upstream repo with the github online functionality, which worked fine.

Now I created a pull request on github, which has merge conflicts.

How can I resolve them locally?

### Response 2

To resolve merge conflicts locally for a pull request, you can follow these steps:

1. Ensure that your local main branch is up to date with the upstream repository:

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

2. Fetch the changes from your forked repository (assuming your remote is named "origin"):

```
git fetch origin
```

3. Check out the branch that has the merge conflicts (in this case, "feature-branch"):

```
git checkout feature-branch
```

4. Merge the main branch into your feature-branch:

```
git merge main
```

Git will highlight the files with merge conflicts.

5. Open the conflicting files in a text editor and look for the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). Resolve the conflicts by manually editing the files, deciding which changes to keep from your branch and which changes to keep from the main branch.

6. After resolving the conflicts, remove the conflict markers and save the files.

7. Stage the resolved files:

```
git add <resolved-file1> <resolved-file2> ...
```

8. Commit the changes:

```
git commit -m "Resolve merge conflicts"
```

9. Push the updated feature-branch to your forked repository:

```
git push origin feature-branch
```

After pushing the changes, the pull request on GitHub should automatically update, and the merge conflicts should be resolved.

If you encounter any issues or have further questions, feel free to ask!
