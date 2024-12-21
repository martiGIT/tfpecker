# tfpecker 🪶

A simple tool for preparing Terraform code for LLM (Large Language Model) analysis. Named after the woodpecker - it pecks through your Terraform files to create a consolidated, AI-friendly output.

## Features

- Combines all Terraform files into a single, easily readable file
- Optionally removes comments for cleaner output
- Optional inclusion of .tfvars and README files
- Security checks for potential secrets with clear warnings
- Respects standard Terraform file structure conventions
- Smart file and directory ignoring
- Deduplication of security warnings

## Installation

```bash
# Clone the repository
git clone https://github.com/martiGIT/tfpecker
cd tfpecker

# Make the script executable (Linux/Mac)
chmod +x tfpecker.py
```

## Usage

Basic usage:
```bash
python tfpecker.py

# or if you made it executable:
./tfpecker.py
```

Options:
```bash
# Specify a different Terraform project path
python tfpecker.py --path /path/to/terraform/project

# Custom output file name (default: terraform_pecked.txt)
python tfpecker.py --output my_terraform.txt

# Remove comments from the output
python tfpecker.py --remove-comments

# Include .tfvars files (disabled by default)
python tfpecker.py --include-tfvars

# Include README files (disabled by default)
python tfpecker.py --include-readme

# All options together
python tfpecker.py --path /project --output output.txt --remove-comments --include-tfvars --include-readme
```

## Security Notice ⚠️

This tool includes basic checks for potential secrets and provides warnings:
1. At the beginning of the output file
2. In the console during execution

The tool will warn you about potential sensitive information such as:
- Tokens and credentials
- API keys
- Passwords
- Access keys
- Secrets
- Other potentially sensitive values

Important security notes:
1. Always verify the output file manually before sharing it with any LLM
2. Never include .tfvars files unless absolutely necessary
3. Be cautious with files that might contain sensitive information
4. Remember that comments might contain sensitive data

## What files are ignored?

tfpecker automatically ignores several types of files and directories for security and clarity:

### Terraform Specific
- *.tfstate files
- *.tfstate.backup
- .terraform directory
- .terraform.lock.hcl
- crash.log
- override.tf
- override.tf.json
- *.tfvars (unless --include-tfvars is specified)
- *.tfvars.json (unless --include-tfvars is specified)
- *.auto.tfvars (unless --include-tfvars is specified)

### Version Control
- .git
- .gitignore
- .svn
- .hg

### IDE and Editor Files
- .idea
- .vscode
- *.swp, *.swo, *.swn
- *~

### OS Specific
- .DS_Store
- Thumbs.db

### Build and Dependencies
- node_modules
- vendor
- __pycache__
- *.pyc

### Logs and Local Development
- *.log files
- logs directory
- .env
- .envrc
- .direnv

### Documentation
- docs directory
- *.md files (except README.md when --include-readme is specified)

## Output Format

The tool generates a single `terraform_pecked.txt` file (by default) with the following structure:

```text
Terraform Infrastructure as Code Package (tfpecker output)
==================================================

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
IMPORTANT: VERIFY FOR SECRETS!
[Security warnings if any sensitive information detected]
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Repository Structure
====================
[List of all included files]

File Contents
====================
[Content of each file with clear separators]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use and modify as needed.

## Name Origin 🪶

The name "tfpecker" comes from combining "tf" (Terraform) with "woodpecker", as the tool pecks through your Terraform files to create a consolidated output, similar to how a woodpecker pecks through wood to find what it needs.
