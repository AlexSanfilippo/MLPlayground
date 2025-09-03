## Installation

To install dependencies use: uv sync for you acelerator
To run pytorch CPU or CUDA GPU, use the follow parameters when syncing UV.

### CPU 

 - uv sync --extra cpu 
 
 
 ### CUDA

 - uv sync --extra cu128


## Using RUFF

 - Format: uv run ruff format

 - Check: uv run ruff check

 - Check automatic fix: uv run ruff check --fix
