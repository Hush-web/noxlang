from setuptools import setup

setup(
    name='noxlang',
    version='2.0.0', 
    description='A plain English automation and AI agent language.',
    author='Adebayo Ayomide Stephen',
    author_email='adebayo2001ayomide@gmail.com',
    url='https://github.com/Hush-web/noxlang',
    py_modules=['engine'],
    install_requires=[
        'lark',
        'python-dotenv',
        'openai'
    ],
    entry_points={
        'console_scripts': [
            'nox=engine:main',
        ],
    },
)