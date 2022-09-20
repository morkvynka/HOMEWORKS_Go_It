from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='Sorting files and folders',
    url='',
    author='Viktoriia Kysliakova',
    author_email='',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:sort']}
)
