from distutils.core import setup

# Dynamically calculate the version based on src.VERSION.
version = __import__('src').get_version()

setup(name='stepic_utils',
      version=version,
      package_dir={'': 'src'},
      packages=['stepic_utils'],
      scripts=['src/stepic_utils/stepicrun.py'],
      )
