# Include configuration file.
include make.conf

.PHONEY: all
all: format test

.PHONEY: clean
clean:
> find project/ -iname '__pycache__' -type d | xargs rm -rf
> find project/ -iname '.mypy_cache' -type d | xargs rm -rf
> find project/ -iname '.pytest_cache' -type d | xargs rm -rf

.PHONEY: format
format:
> @ # Execute in silence.
> yapf -irp -vv --no-local-style project/ampyr

.PHONEY: test
test: test_pytests test_coverage

.PHONEY: test_pytests
test_pytests:
> pytest project/ -l -vv --full-trace \
>   --durations=0 --junit-xml=pytest-results.xml
> genbadge tests -t 80.00 \
>   -i pytest-results.xml -o project/assets/pytest-results.svg

.PHONEY: test_coverage
test_coverage:
> pytest project/ --no-summary --no-header -q   \
>   --cov --cov-report=xml:pytest-coverage.xml --cov-branch
> genbadge coverage -i pytest-coverage.xml \
>   -o project/assets/pytest-coverage.svg
