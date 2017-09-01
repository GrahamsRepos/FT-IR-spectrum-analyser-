import setuptools
from setuptools import setup
from setuptools import find_packages

setup(name='FT-I.R. Spectra Analyser',
      version='0.1',
      description='Simple Discrete Fourier Transform Tool For Infrared Spectra',
      url='http://github.com/GrahamNash/FT-IR-spectrum-analyser-',
      author='Graham Nash',
      author_email='GrahamDevelopmentMail@gmail.com',
      license='Open Source',
      packages=find_packages(),
      zip_safe=False,
      install_requires=(['qt == 4.8.7', 'pyqt == 4.11.4', 'pyqtgraph']),
      include_package_data=True)
