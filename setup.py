import os
import re

import pkg_resources
from setuptools import setup, find_packages

def parse_requirements(filename):
    """Parse requirements.txt, handling git+ URLs and other VCS references."""
    requirements = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Handle git+ URLs and other VCS requirements
            if line.startswith('git+') or line.startswith('svn+') or line.startswith('hg+') or line.startswith('bzr+'):
                # Extract package name from VCS URL if possible
                # For git+https://github.com/user/repo.git@branch#egg=package_name
                egg_match = re.search(r'#egg=([^&]+)', line)
                if egg_match:
                    package_name = egg_match.group(1)
                    requirements.append(f"{package_name} @ {line}")
                else:
                    # If no egg specified, try to extract from URL
                    # This is a fallback and might not work for all cases
                    url_match = re.search(r'git\+https?://[^/]+/([^/]+)/([^/.]+)(?:\.git)?', line)
                    if url_match:
                        package_name = url_match.group(2)
                        requirements.append(f"{package_name} @ {line}")
                    else:
                        # If we can't determine the package name, add the URL as is
                        requirements.append(line)
            else:
                # Regular requirement
                requirements.append(line)
    
    return requirements

setup(
    name="RealESRGAN",
    py_modules=["RealESRGAN"],
    version="1.0",
    description="",
    author="Sberbank AI, Xintao Wang",
    url='https://github.com/ai-forever/Real-ESRGAN',
    packages=find_packages(include=['RealESRGAN']),
    install_requires=parse_requirements(
        os.path.join(os.path.dirname(__file__), "requirements.txt")
    ),
    dependency_links=[],  # Deprecated in newer setuptools, but kept for compatibility
                    )
