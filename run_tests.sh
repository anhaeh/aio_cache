#/bin/bash
coverage run --source=aio_cache -m pytest
TEST_EXIT_STATUS=$?
coverage report -m
rm .coverage
exit $TEST_EXIT_STATUS
