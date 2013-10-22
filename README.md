# Recent Earthquakes, Group 11

This is our submission for the Stat157 assignment posted [here](https://github.com/stat157/recent-quakes).

## Setup Instructions

Follow the initial setup instructions on the [Stat157 GitHub Page](https://github.com/stat157/recent-quakes).

Then execute the following commands in your virtual machine:

```sh
git clone git@github.com:reenashah/recent-quakes-Group11.git

cd recent-quakes-Group11/

git clone git@github.com:reenashah/recent-quakes-Group11-data.git data
```

The first command cloned our source code ("recent-quakes-Group11").  The third command created a directory called "data" and cloned our [data repository](https://github.com/reenashah/recent-quakes-Group11-data) into the source code directory.

Now you are ready to run the ipython notebook.  Type the following command at your terminal:

```sh
ipython notebook --no-browser --ip=0.0.0.0 --script --pylab=inline &
```

