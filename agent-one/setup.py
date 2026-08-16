"""Setup script for Agent One"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-one",
    version="1.0.0",
    author="Agent One",
    description="Autonomous video processing agent for multi-platform content creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.7.0",
        "google-auth>=2.25.0",
        "google-auth-oauthlib>=1.1.0",
        "google-auth-httplib2>=0.2.0",
        "google-api-python-client>=2.100.0",
        "openai>=1.3.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "agent-one=agent:main",
        ],
    },
)
