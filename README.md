# compute_graph

Data analysis generally involves taking some source data and performing some series of operations upon it until you have reached your desired output. Sometimes, that data is bigger than any one computer can handle. This library provides a simple serialization system for data analysis, which can then be used to pass around the specific set of tasks to be accomplished and handled appropriately on the backend.

## Releasing

#### Set up

If this is the first time you have done a conda release make sure the following prerequisites are met:
1. You will need the anaconda client and the build package.
  * `conda install -q anaconda-client conda-build`
2. Make sure automatic uploads are turned off. 
  * `conda config --set anaconda_upload no`
3. If you are behind a corporate firewall that intercepts ssl you may need to turn ssl off. 
  * `conda config --set ssl_verify False`
  * `anaconda config --set verify_ssl False`
  
#### Version and Build

To set the version for the release simply edit `conda/meta.yaml` and set the version per semantic versioning rules.
The `git_tag` should be changed to match what will be in the release in github. This can match the semantic version.

Inside the root of the project directory, run `conda build .`. This will find the project and build the software.
  * _Conda will note that it was told not to upload. Copy down the .tar.bz2 path, we need it later._
  
At this point it is a good idea to create an empty environment and give the software a quick test.
  * `conda create -n test_env`
  * `source activate test_env`
  * `conda install compute_graph --use-local`
  * `python2`
  * `import compute_graph` etc...
  
#### Uploading

Push the changes to github, and verify that the build passes on CircleCI.

Create a new [release](https://github.com/CDAT/compute_graph/releases) on github.
  * The tag here must match the `git_tag` in the `meta.yaml` exactly!

Run `anaconda -t $TOKEN upload -u cdat $PATH`
  * $TOKEN comes from https://anaconda.org/cdat/settings/access
  * $PATH should look something like `/Users/your_user/miniconda2/conda-bld/noarch/compute_graph-0.0.0-py_0.tar.bz2`
  
Check https://anaconda.org/cdat/compute_graph/files to verify that the new version is available.
