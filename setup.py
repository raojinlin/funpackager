import setuptools


with open('README.md', 'rt') as readme:
    long_description = readme.read()


setuptools.setup(
    name='funpackager',
    version='0.0.0',
    author='raojinlin',
    author_email='1239015423@qq.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=[
        'funpackager',
        'funpackager/bin/*'
    ]),
    scripts=['funpackager/bin/funpackager'],
    install_requires=[
        'PyYAML'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
