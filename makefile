# Include configuration file.
include make.conf


.PHONEY: clean
clean:
> @ # Execute in silence.
> find project/ -iname '__pycache__' -type d | xargs rm -rf
> find project/ -iname '.mypy_cache' -type d | xargs rm -rf
> find project/tests/ -iname '*.xml' -type f | xargs rm

.PHONEY: test
test: test_pytests

.PHONEY: test_pytests
test_pytests:
> @ # Execute in silence.
> pytest project/ -l \
>     --full-trace   \
>     --durations=0  \
>     --junit-xml=project/tests/ampyr-pytest.xml \
>     --cov --cov-report=xml --cov-branch
> mv coverage.xml project/tests/ampyr-coverage.xml
