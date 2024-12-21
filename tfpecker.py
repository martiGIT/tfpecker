import os
import glob
from pathlib import Path
from typing import List, Set
import argparse

class TerraformPacker:
    """Tool for packing Terraform code for LLM analysis."""
    
    def __init__(self, base_path: str = ".", output_file: str = "terraform_pecked.txt", 
                 remove_comments: bool = False, include_tfvars: bool = False, include_readme: bool = False):
        self.base_path = Path(base_path)
        self.output_file = output_file
        self.remove_comments = remove_comments
        self.include_tfvars = include_tfvars
        self.include_readme = include_readme
        self.default_ignore = {
            # Terraform specific
            "*.tfstate",
            "*.tfstate.backup",
            ".terraform",
            ".terraform.lock.hcl",
            "crash.log",
            "override.tf",
            "override.tf.json",
            
            # Version control
            ".git",
            ".gitignore",
            ".svn",
            ".hg",
            
            # IDE and editor files
            ".idea",
            ".vscode",
            "*.swp",
            "*.swo",
            "*.swn",
            "*~",
            
            # OS specific
            ".DS_Store",
            "Thumbs.db",
            
            # Build and dependency directories
            "node_modules",
            "vendor",
            "__pycache__",
            "*.pyc",
            
            # Log files
            "*.log",
            "logs",
            
            # Local development
            ".env",
            ".envrc",
            ".direnv",
            
            # Documentation (unless explicitly included)
            "docs",
            "*.md",
        }
        if not include_tfvars:
            self.default_ignore.update({"*.tfvars", "*.tfvars.json", "*.auto.tfvars"})

    def find_relevant_files(self) -> List[Path]:
        """Find all relevant files in the directory."""
        relevant_files = []
        
        # Search for .tf files
        for path in self.base_path.rglob("*.tf"):
            if not any(ignore in str(path) for ignore in self.default_ignore):
                relevant_files.append(path)
        
        # Include .tfvars if specified
        if self.include_tfvars:
            for pattern in ["*.tfvars", "*.tfvars.json", "*.auto.tfvars"]:
                for path in self.base_path.rglob(pattern):
                    if not any(ignore in str(path) for ignore in self.default_ignore):
                        relevant_files.append(path)
        
        # Include README files if specified
        if self.include_readme:
            self.default_ignore.remove("*.md")  # Temporarily remove .md from ignore list
            readme_patterns = ["README.md", "README.markdown", "Readme.md"]
            for pattern in readme_patterns:
                for path in self.base_path.rglob(pattern):
                    if not any(ignore in str(path) for ignore in self.default_ignore):
                        relevant_files.append(path)
            self.default_ignore.add("*.md")  # Add back .md to ignore list
                
        return sorted(relevant_files)

    def remove_terraform_comments(self, content: str) -> str:
        """Remove both single-line and multi-line comments from Terraform code."""
        import re
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove single-line comments (but keep commented-out resource blocks)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if not line.lstrip().startswith('#'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def warn_about_potential_secrets(self, content: str) -> List[str]:
        """Basic check for potential secrets in the content."""
        warnings = []
        keywords = ['password', 'secret', 'key', 'token', 'credential', 'api_key', 'access_key']
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in keywords):
                warnings.append(f"Line {i} might contain sensitive information: {line.strip()}")
        
        return warnings

    def pack_files(self):
        """Pack all Terraform files into a single output file."""
        files = self.find_relevant_files()
        all_warnings = []
        
        with open(self.output_file, "w", encoding="utf-8") as output:
            # Write header
            output.write("Terraform Infrastructure as Code Package (tfpecker output)\n")
            output.write("=" * 50 + "\n\n")
            
            # Write security warning at the top if any issues found
            output.write("!" * 50 + "\n")
            output.write("IMPORTANT: VERIFY FOR SECRETS!\n")
            output.write("Double-check this file before sharing with LLM models to ensure no secrets or sensitive data are included.\n")
            
            # First scan all files for warnings
            for file in files:
                relative_path = file.relative_to(self.base_path)
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        content = f.read()
                        warnings = self.warn_about_potential_secrets(content)
                        if warnings:
                            all_warnings.extend([f"{relative_path}: {w}" for w in warnings])
                except Exception as e:
                    print(f"Error reading file for security check: {e}")

            if all_warnings:
                output.write("\nPotential sensitive information detected:\n")
                for warning in all_warnings:
                    output.write(f"- {warning}\n")
                
                # Also print warnings to console
                print("\n" + "!" * 50)
                print("⚠️  SECURITY WARNING: Potential sensitive information detected:")
                for warning in all_warnings:
                    print(f"- {warning}")
                print("!" * 50 + "\n")
                    
            output.write("!" * 50 + "\n\n")
            
            # Write structure
            output.write("Repository Structure\n")
            output.write("=" * 20 + "\n\n")
            
            for file in files:
                relative_path = file.relative_to(self.base_path)
                output.write(str(relative_path) + "\n")
            
            output.write("\nFile Contents\n")
            output.write("=" * 20 + "\n\n")
            
            for file in files:
                relative_path = file.relative_to(self.base_path)
                output.write(f"File: {relative_path}\n")
                output.write("-" * (len(str(relative_path)) + 6) + "\n\n")
                
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if self.remove_comments:
                            content = self.remove_terraform_comments(content)
                        
                        # Check for potential secrets
                        warnings = self.warn_about_potential_secrets(content)
                        if warnings:
                            all_warnings.extend([f"{relative_path}: {w}" for w in warnings])
                            
                        output.write(content)
                except Exception as e:
                    output.write(f"Error reading file: {e}")
                
                output.write("\n\n")
            
            # Add warning about verifying secrets
            output.write("\n" + "!" * 50 + "\n")
            output.write("IMPORTANT: VERIFY FOR SECRETS!\n")
            output.write("Double-check this file before sharing with LLM models to ensure no secrets or sensitive data are included.\n")
            if all_warnings:
                output.write("\nPotential sensitive information detected:\n")
                for warning in all_warnings:
                    output.write(f"- {warning}\n")
            output.write("!" * 50 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="tfpecker - Pack Terraform code for LLM analysis while helping prevent secret exposure"
    )
    parser.add_argument("--path", "-p", default=".", help="Path to Terraform project")
    parser.add_argument("--output", "-o", default="terraform_pecked.txt", 
                       help="Output file name")
    parser.add_argument("--remove-comments", "-rc", action="store_true",
                       help="Remove comments from Terraform files")
    parser.add_argument("--include-tfvars", "-tv", action="store_true",
                       help="Include .tfvars files in the output")
    parser.add_argument("--include-readme", "-ir", action="store_true",
                       help="Include README files in the output")
    
    args = parser.parse_args()
    
    packer = TerraformPacker(args.path, args.output, args.remove_comments, args.include_tfvars, args.include_readme)
    packer.pack_files()
    print(f"Terraform code packed to {args.output}")
    print("⚠️  Please verify the output file for any sensitive information before sharing!")

if __name__ == "__main__":
    main()
