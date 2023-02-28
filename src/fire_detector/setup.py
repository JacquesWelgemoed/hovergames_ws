from setuptools import setup

package_name = 'fire_detector'

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
    maintainer='jacques',
    maintainer_email='jacques@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'fire_sub = fire_detector.fire_sub:main',
                'fire_sniffer = fire_detector.fire_sniffer:main',
                'client_test = fire_detector.client_test:main',
        ],
    },
)
