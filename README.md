
# setmlvis

[![Build Status](https://travis-ci.org/VisDunneRight/setmlvis.svg?branch=master)](https://travis-ci.org/VisDunneRight/setmlvis)
[![codecov](https://codecov.io/gh/VisDunneRight/setmlvis/branch/master/graph/badge.svg)](https://codecov.io/gh/VisDunneRight/setmlvis)

A new visualization method for comparing different models for bounding box detection.

## Installation

You can install using `pip`:

```bash
pip install setmlvis
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:

```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] setmlvis
```

## Development Installation

Create a dev environment:

1. Conda

    ```bash
    conda create -n setmlvis-dev -c conda-forge nodejs yarn python jupyterlab
    conda activate setmlvis-dev
    ```

2. `venv`

    ```bash
    py -m venv env
    .\env\Scripts\activate
    ```

Install the python. This will also build the TS package.

```bash
pip install -e ".[test, examples]"
```

You will need `jupyter lab` 3.x or `jupyter notebook` installed. If you don't have it, run, e.g.:

```bash
pip install jupyterlab<4
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. You need `yarn` installed first. If you don't, run:

```bash
npm install yarn
```

Then, to enable the extensions for lab, run the command:

```bash
jupyter labextension develop --overwrite .
```

and

```bash
yarn run build
```

or

```bash
.\node_modules\yarn\bin\yarn run build
```

For classic notebook, you need to run:

```bash
jupyter nbextension install --sys-prefix --symlink --overwrite --py setmlvis
jupyter nbextension enable --sys-prefix --py setmlvis
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### How to see your changes
#### Typescript:
If you use JupyterLab to develop then you can watch the source directory and run JupyterLab at the same time in different
terminals to watch for changes in the extension's source and automatically rebuild the widget.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.

## Updating the version

To update the version, install tbump and use it to bump the version.
By default it will also create a tag.

```bash
pip install tbump
tbump <new-version>
```

