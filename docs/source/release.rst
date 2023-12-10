
.. _release:

Release Process
===============

#. Update the versions in ``package.json``, ``setmlvis/_version.py``, and ``setmlvis/_frontend.py``.
#. Possibliy update versions in ``pyproject.toml`` and ``package_lock.json``
#. Make a release commmit: ``git add . && git commit -m "release vX.Y.Z"``
#. Tag the commit: ``git tag vX.Y.Z``
#. Push the commit and tag: ``git push && git push --tags``
#. Release the npm packages: ``npm login`` and ``npm publish``
#. Bundle the Python package: ``pip install build twine``
#. build the Python package: ``python -m build .``
#. Publish the package to PyPI: ``twine upload dist/setmlvis-X.Y.Z*``
