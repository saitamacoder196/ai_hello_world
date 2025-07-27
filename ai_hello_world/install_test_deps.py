#!/usr/bin/env python3
"""
Install test dependencies for AI Hello World project.
Handles different environments and platform-specific issues.
"""

import subprocess
import sys
import os

def install_package(package_name, version=None):
    """Install a single package with error handling."""
    if version:
        package_spec = f"{package_name}=={version}"
    else:
        package_spec = package_name
    
    try:
        print(f"Installing {package_spec}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_spec],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Successfully installed {package_spec}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_spec}")
        print(f"Error: {e.stderr}")
        return False

def check_package(package_name):
    """Check if a package is already installed."""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def main():
    """Main installation function."""
    print("🔧 Installing test dependencies for AI Hello World...")
    print("=" * 60)
    
    # Essential test dependencies
    test_deps = [
        ("factory_boy", "factory-boy", "3.3.1"),
        ("faker", "Faker", None),
    ]
    
    all_success = True
    
    for import_name, package_name, version in test_deps:
        if not check_package(import_name):
            success = install_package(package_name, version)
            if not success:
                all_success = False
    
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 All test dependencies installed successfully!")
        print("\nYou can now run tests with:")
        print("  python run_tests.py")
        print("  python manage.py test tests/")
    else:
        print("💥 Some dependencies failed to install")
        print("\nManual installation steps:")
        print("1. Try: pip install factory-boy")
        print("2. Or: pip install --user factory-boy")
        print("3. Or: conda install factory-boy (if using conda)")
        
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())