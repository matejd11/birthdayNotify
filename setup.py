from setuptools import setup, find_packages

setup(
        name='birthdayNotify',
        version='1.0',
        description='notification of birthdays',
        author='Matej Dujava',
        author_email='mdujava@gmail.com',
        url='https://github.com/matejd11/birthdayNotify',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: Unix',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        packages=find_packages(exclude=['docs', 'tests*']),
        install_requires=[
            'numpy',
        ],
        entry_points={'console_scripts': ['birthdayNotify = birthdayNotify.main:main']}
)
