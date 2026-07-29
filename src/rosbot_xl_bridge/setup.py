import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'rosbot_xl_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # The "Magic" lines that include your Webots files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'resource'), glob(os.path.join('resource', '*.urdf'))),
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.wbt'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jkeo22',
    maintainer_email='your_email@example.com',
    description='Webots ROS 2 bridge for Rosbot XL',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rosbot_driver = rosbot_xl_bridge.rosbot_driver:main'
        ],
    },
)

