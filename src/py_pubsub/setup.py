from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jkeo22',
    maintainer_email='jkeosourinha@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.subscriber_member_function:main',
            'seer = py_pubsub.seer:main',
            'doer = py_pubsub.doer:main',
            'mover = py_pubsub.mover:main',
            'wall_avoider = py_pubsub.wall_avoider:main',
            'obstacle_avoider = py_pubsub.obstacle_avoider:main',
        ],
    },
)
