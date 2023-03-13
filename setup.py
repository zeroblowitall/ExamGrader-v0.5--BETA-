from setuptools import setup, find_packages

setup(
    name='Spindley ExamGrader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'PyQt5',
    ],
    entry_points={
        'console_scripts': [
            'exam_grader_gui=exam_grader_gui:main',
        ],
    },
)
