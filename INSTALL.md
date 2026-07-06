# Install Fixed Profile README

This version fixes the broken repository-card image problem.

## What changed?

The old Featured Repositories section used image cards like:

```md
<img src="https://github-readme-stats.vercel.app/api/pin/?username=vibhug0077&repo=Python_Programing" />
```

Those external SVG images may fail, so GitHub displays only the alt text.

This fixed version uses normal Markdown/HTML cards instead. They are reliable because they do not depend on an external repo-card image service.

## Folder structure

```text
vibhug0077/
├── README.md
├── scripts/
│   └── update_profile_readme.py
└── .github/
    └── workflows/
        └── update-profile-readme.yml
```

## Apply

```bash
git clone https://github.com/vibhug0077/vibhug0077.git
cd vibhug0077

# Copy these files into the repository, then:

git add README.md scripts/update_profile_readme.py .github/workflows/update-profile-readme.yml
git commit -m "fix: replace broken repo-card images with reliable profile cards"
git push
```

## Test manually

```bash
python scripts/update_profile_readme.py
```

Or run from GitHub:

```text
Actions → Update Profile README → Run workflow
```
