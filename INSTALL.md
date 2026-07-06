# Installation Guide

Use these files in your special GitHub profile repository:

```text
vibhug0077/
├── README.md
├── scripts/
│   └── update_profile_readme.py
└── .github/
    └── workflows/
        └── update-profile-readme.yml
```

## Steps

```bash
git clone https://github.com/vibhug0077/vibhug0077.git
cd vibhug0077
```

Copy the generated files into this repository, then run:

```bash
git add README.md scripts/update_profile_readme.py .github/workflows/update-profile-readme.yml
git commit -m "feat: redesign dynamic GitHub profile README"
git push
```

## Test the dynamic script locally

```bash
python scripts/update_profile_readme.py
```

## Run manually from GitHub

Go to:

```text
Actions → Update Profile README → Run workflow
```

The workflow also runs daily at 08:00 IST.
