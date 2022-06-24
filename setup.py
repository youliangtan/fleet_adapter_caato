from setuptools import setup

package_name = 'fleet_adapter_caato'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Samuel',
    maintainer_email='samuelangdj@gmail.com',
    description='RMF fleet adapter for Caato robots',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fleet_adapter_caato=fleet_adapter_caato.fleet_adapter_caato:main',
            'fleet_adapter_ecobot=fleet_adapter_ecobot.fleet_adapter_ecobot:main',
            'clicked_point_transform=fleet_adapter_ecobot.clicked_point_transform:main',
        ],
    },
)
