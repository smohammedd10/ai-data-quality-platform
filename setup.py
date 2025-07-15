from setuptools import setup, find_packages

setup(
    name='ai_data_quality_platform',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pandas',
        'openai',
        'streamlit',
        'apache-airflow',
        'great_expectations==0.18.7',
        'boto3',
        'pyarrow',
        's3fs'
    ],
    entry_points={
        'console_scripts': []
    },
    author='Your Name',
    description='LLM-powered Data Quality Platform with Great Expectations + Airflow + Streamlit',
    keywords='data-quality gpt openai great-expectations airflow glue',
    license='MIT',
)
