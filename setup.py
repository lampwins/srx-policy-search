from distutils.core import setup

setup(
    name='srxpolicysearch',
    version='0.0.6',
    packages=['srxpolicysearch'],
    url='https://github.com/lampwins/srx-policy-search',
    license='MIT',
    author='John Anderson',
    author_email='lampwins@gmail.com',
    description='Search security policy on the Juniper SRX platform',
    install_requires=['paramiko']
)
