# Include configuration file.
include make.conf


.PHONEY: clean
clean:
> @ # Execute in silence.
> find project/ -iname '__pycache__' -type d | xargs rm -rf
> find project/ -iname '.mypy_cache' -type d | xargs rm -rf

.PHONEY: test
test: test_pytests test_coverage

.PHONEY: test_pytests
test_pytests:
> @ # Execute in silence.
> pytest project/ -l -vv --full-trace --durations=0

.PHONEY: test_coverage
test_coverage:
> @ # Execute in silence.
> pytest project/ --no-summary --no-header -q   \
>   --cov --cov-report=xml:cov.xml --cov-branch
