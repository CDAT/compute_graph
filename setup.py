import os
from setuptools import setup


setup(
  name="compute_graph",
  version="0.0.1",
  description="A graph-based representation of operations performed on source data to generate data products.",
  url="http://github.com/UV-CDAT/compute_graph",
  packages=['compute_graph'],
  package_dir={'compute_graph': 'src'},
  test_suite='nose.collector',
  setup_requires=["nose"],
  tests_require=['nose', 'coverage']
)
