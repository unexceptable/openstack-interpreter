from setuptools import setup

with open('requirements.txt') as f:
    required = f.readlines()

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='openstack-interpreter',

    version='0.1.3',
    description='A simple command to drop you into the python interpreter '
                'with the openstack easy to setup.',
    long_description=long_description,
    url='https://github.com/Adrian-Turjak/openstack-interpreter',
    author='Adrian Turjak',
    author_email='adriant@catalyst.net.nz',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: OpenStack',
    ],

    keywords='openstack python interpreter clients',
    py_modules=['openstack_interpreter'],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'os-interpreter = openstack_interpreter:setup',
        ],
    }
)
