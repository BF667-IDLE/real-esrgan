import os
import re
from pathlib import Path

from setuptools import setup, find_packages

def parse_requirements(filename):
    """Parse requirements.txt, handling git+ URLs and other VCS references."""
    requirements = []
    requirements_file = Path(__file__).parent / filename
    
    if not requirements_file.exists():
        return []
    
    with open(requirements_file) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Handle git+ URLs and other VCS requirements
            if line.startswith(('git+', 'svn+', 'hg+', 'bzr+')):
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
                # Handle environment markers and extras
                if ';' in line:
                    requirements.append(line)
                else:
                    # Ensure we don't have pkg_resources as a requirement
                    if not line.startswith('pkg_resources'):
                        requirements.append(line)
    
    return requirements

# Read version from file or set default
__version__ = "1.0"
version_file = Path(__file__).parent / "version.txt"
if version_file.exists():
    __version__ = version_file.read_text().strip()

setup(
    name="RealESRGAN",
    py_modules=["RealESRGAN"],
    version=__version__,
    description="Real-ESRGAN: Practical Algorithms for General Image/Video Restoration",
    author="Sberbank AI, Xintao Wang",
    author_email="xintao.wang@outlook.com",
    url='https://github.com/ai-forever/Real-ESRGAN',
    license="BSD-3-Clause",
    packages=find_packages(include=['RealESRGAN', 'RealESRGAN.*']),
    python_requires='>=3.12',
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Graphics',
    ],
    entry_points={
        'console_scripts': [
            'realesrgan=RealESRGAN.realesrgan:main',  # Adjust based on your actual entry point
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
