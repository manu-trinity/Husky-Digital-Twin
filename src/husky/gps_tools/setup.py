from setuptools import setup

package_name = 'gps_tools'

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
    description='GPS verification tools for Husky simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gps_verifier = gps_tools.gps_verifier:main',
        ],
    },
)
