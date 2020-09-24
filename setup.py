import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='reporter-MAKSIM-SHAVRIN',  # Replace with your own username
    version='0.0.1',
    author="Maksim Shavrin",
    author_email="nutmegraw@gmail.com",
    description="counting Q1 result times from log files of the Formula 1 - Monaco 2018 Racing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/orahmudri/task-6-report-of-monaco-2018-racing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: Freeware',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
