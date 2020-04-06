from setuptools import setup, find_packages

version = '0.1.0'

install_requires = [
    'certbot>=1.0.0',
    'acme',
    'setuptools',
    'requests'
]

desc = 'Cynthia ACME Validation Service plugin for Certbot'

setup(
    name='certbot-dns-cavs',
    version=version,
    description=desc,
    long_description=desc,
    long_description_content_type='text/plain',
    url='https://github.com/bitcynth/certbot-dns-cavs',
    author='Cynthia Revstrom',
    author_email='me+cavs@cynthia.re',
    license='MIT License',
    python_requires='>=3.5',
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-cavs = certbot_dns_cavs.dns_cavs:Authenticator'
        ]
    }
)