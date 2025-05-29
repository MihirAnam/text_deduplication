from setuptools import setup, find_packages

setup(
    name='text_deduplicator',
    version='0.1.0',
    description='A utility for text deduplication using TF-IDF and cosine similarity.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
