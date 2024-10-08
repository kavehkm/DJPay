from setuptools import setup
setup(
    name="djpay",
    version="1.0.0",
    packages=["djpay"],
    include_package_data=True,
    install_requires=[
        "Django>=5.1.1",
    ],
    author="Kaveh Mehrbanian",
    author_email="mehrbaniankaveh@gmail.com",
    description="A reusable Django app for handling various type of paying methods",
    url="https://github.com/kavehkm/DJPay",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
