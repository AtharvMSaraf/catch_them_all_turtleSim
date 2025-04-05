from setuptools import find_packages, setup

package_name = 'catch_them_all'

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
    maintainer='atharvsaraf',
    maintainer_email='atharvmakarandsaraf@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "respawn=catch_them_all.turtle_respawn_service:main",
            "get_main_turtle_pose = catch_them_all.turtle_position_tracker:main"
            "get_pose = catch_them_all.turtle_pose_service:main "
        ],
    },
)
