Usage
=====

Build the generated bindings and Sphinx HTML locally:

.. code-block:: bash

   uv sync
   uv run python scripts/build_docs.py

The generated HTML site will be written to ``docs/_build/html``.

The documentation build imports the generated UniFFI Python modules, so it must run after the native ``matrix-sdk-ffi`` library and Python bindings have been generated.
