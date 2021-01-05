Releasing a new version
=======================

To release a new version of the package to PyPi,

1. Make sure CHANGELOG.rst is up to date with any changes from the previously
   released version.

2. Go to https://github.com/predsci/PsiPy/releases/new

3. Fill in the version number. If there is new functionality, bump the second
   number and reset the third (e.g. 0.1.2 > 0.2.0). If this is a minor update,
   just bump the third number (e.g. 0.1.2 > 0.1.3)

4. Put "PsiPy *version*" in the release title, replacing *version* with the
   version number.

5. Click "Publish release". Through the magic of github actions, the package
   will automatically be built and uploaded to PyPi.
