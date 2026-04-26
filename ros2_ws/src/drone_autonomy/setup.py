from setuptools import find_packages, setup

package_name = 'drone_autonomy'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/slam.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sandhm1',
    maintainer_email='manjotssandhu1@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "slam_monitor = drone_autonomy.slam_monitor:main",
            "px4_odom_bridge = drone_autonomy.px4_odom_bridge:main",
        ],
    },
)