from setuptools import setup, find_packages

setup(
    name="Explain",
    version="0.0.1",
    author="Maya Lekhi",
    author_email="maya.lekhi1@gmail.com",
    description="The quickest solution for repository analysis",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mlekhi/summarize",
    project_urls={
        "Homepage": "https://github.com/mlekhi/summarize",
        "Issues": "https://github.com/mlekhi/summarize/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "openai",
        "python-dotenv",
        "requests"
    ],
)
