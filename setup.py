import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from shutil import copyfile


class InstallScriptCommand(install):
    def run(self):
        install.run(self)
        self.install_script()

    def install_script(self):
        home_dir = os.path.expanduser("~")
        target_dir = os.path.join(home_dir, ".oslui")
        source_path = os.path.join("build/lib/oslui", "scripts/record_command.sh")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        script_path = os.path.join(target_dir, "record_command.sh")
        copyfile(source_path, script_path)


setup(
    name='oslui',
    version='0.1.9',
    url='https://github.com/BalianWang/OSLUI',
    author='BalianWang',
    author_email='balian.wang1997@gmail.com',
    description='Natural Language User Interface for Operating Systems',
    packages=find_packages(),
    package_data={'oslui': ['scripts/record_command.sh']},
    install_requires=[
        'pydantic',
        'rich',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'oslui = oslui.main:main',
        ],
    },
    cmdclass={
        'install': InstallScriptCommand,
    },
    license='MIT',
    python_requires='>=3'
)
