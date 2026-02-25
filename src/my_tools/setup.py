from setuptools import setup # type: ignore
import os
from glob import glob

package_name = 'my_tools'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='trinity',
    maintainer_email='manu.benny@st.ovgu.de',
    description='my tools',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'position_verifier = my_tools.position_verifier:main',
    ],
},
)
