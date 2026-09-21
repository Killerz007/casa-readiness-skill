# Publishing the repository

Suggested public repository name: `casa-readiness-skill`.

If using GitHub CLI from a local checkout:

```bash
gh repo create casa-readiness-skill --public --source=. --remote=origin --push
```

If creating the repository in the GitHub UI, create an empty public repository without an auto-generated README/LICENSE, then push this checkout:

```bash
git remote add origin git@github.com:<owner>/casa-readiness-skill.git
git push -u origin main
```

After publishing, verify that GitHub Actions is enabled and that the scheduled workflow has `contents`, `pull-requests`, and `issues` write permissions as defined in the workflow. The first manual run of **Monthly CASA upstream sync** will populate `official/current/` and the generated test-case catalogue from the latest released upstream source.
