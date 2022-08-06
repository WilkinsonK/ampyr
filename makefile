# Include configuration file.
include make.conf


.PHONEY: clean
clean:
> @ # Execute in silence.
> find project/ -iname '__pycache__' -type d | xargs rm -rf
> find project/ -iname '.mypy_cache' -type d | xargs rm -rf
