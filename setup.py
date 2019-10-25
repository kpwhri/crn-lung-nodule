from distutils.core import setup
import setuptools

setup(name='crn_lung_nodule',
      version='0.2',
      description='NLP module for identifying lung nodules.',
      url='https://bitbucket.org/dcronkite/crn-lung-nodule',
      author='dcronkite',
      author_email='dcronkite-gmail',
      license='MIT',
      classifiers=[  # from https://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Programming Lpanguage :: Python :: 3 :: Only',
      ],
      keywords='nlp information extraction',
      entry_points={
          'console_scripts':
              [
                  'crn-algorithm = crn_lung_nodule.__main__:main',
              ]
      },
      install_requires=['nltk'],
      package_dir={'': 'src'},
      packages=setuptools.find_packages('src'),
      package_data={'crn_lung_nodule': ['data/keywords.db', 'data/ssplit.db']},
      zip_safe=False
      )
