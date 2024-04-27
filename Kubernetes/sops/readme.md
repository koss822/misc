# SOPS Git Hooks for Kubernetes Secrets Management

This guide provides an overview and setup instructions for using Git hooks with Mozilla's SOPS (Secrets OperationS) for managing Kubernetes secrets. The Git hooks are designed to automate the encryption and decryption of sensitive fields in YAML files, specifically targeting password and value attributes, to securely manage configuration in version control.

## Why Use It

In the context of Kubernetes and infrastructure management, keeping sensitive configuration out of Git repositories is a critical security practice. However, managing these secrets externally can complicate configuration management and deployment workflows.

Integrating SOPS with Git hooks provides an automated way to securely manage secrets within Git repositories by encrypting sensitive information before it's committed and decrypting it upon checkout.

## Benefits

* **Security**: Automatically encrypt sensitive fields before committing to Git, reducing the risk of exposing sensitive information.
* **Automation**: Streamline the process of working with encrypted configuration, making it transparent and error-resistant.
* **Version Control for Secrets**: Keep encrypted versions of secrets in version control, allowing for better tracking of changes and access to historical versions.

## Disadvantages

* **Setup Complexity**: Initial setup of encryption keys and Git hooks requires some manual steps and understanding of security practices.
* **Environment Specifics**: Needs careful handling of encryption keys and ensuring they are securely managed and accessible in the required environments.

## How It Was Written

The Git hooks were created to fulfill the need for a secure, automated way to manage Kubernetes secrets in version control. Recognizing the importance of securing sensitive information while minimizing disruption to development workflows, these hooks integrate seamlessly with SOPS and Git, providing an efficient solution for encrypting and decrypting sensitive fields in YAML files.

## Setup Instructions
### Generating AGE Keys

First, you need to generate a pair of AGE keys (public and private) for SOPS to use during encryption and decryption.

1. Install age (https://github.com/FiloSottile/age) 
```bash
brew install age
```

2. Generate a new age keypair
```bash
age-keygen -o age_key.txt
```

3. Separate the public and private keys
```bash
cat age_key.txt | grep "public key" > age_public.key
cat age_key.txt | grep -v "public key" > age_private.key
```

### Preparing the .sops Directory

1. Create a .sops directory in your project root and move your AGE keys there:

```bash
mkdir -p .sops/age
mv age_public.key .sops/age/public.key
mv age_private.key .sops/age/private.key
```

### Copying Git Hooks

1. Copy the provided pre-commit and post-checkout hook scripts into the .git/hooks directory of your repository, ensuring they are executable.

# Example for pre-commit
```bash
cp pre-commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

# Example for post-checkout
```bash
cp post-checkout.sh .git/hooks/post-checkout
chmod +x .git/hooks/post-checkout
```

These scripts automatically encrypt fields marked as password or value in .yml files on commit and decrypt them on checkout.
Usage Examples

Once setup, the encryption and decryption process is automated through the Git hooks.

### Adding a New Secret:

Add or modify your Kubernetes .yml configuration file, including secrets with password or value fields.
Stage and commit your changes. The pre-commit hook will automatically encrypt your secrets.

```bash

git add my-secrets.yml
git commit -m "Add encrypted secret"
```

Your secrets are now encrypted in the repository.

### Cloning and Working with the Repository:

When you clone the repository or checkout a commit, the post-checkout hook will automatically decrypt any encrypted .yml files.

```bash
git checkout main
```

Work with your configuration files as needed. Modifications to secrets will be re-encrypted on the next commit.

## Conclusion

Integrating SOPS with Git hooks provides a seamless and secure method for managing Kubernetes secrets within Git, automating the process of encrypting and decrypting sensitive information in your configuration files. While the initial setup requires careful handling of encryption keys, the benefits of secure, version-controlled secrets management significantly outweigh the initial complexity.
