"""
prefect deployment build \
	src/flow/f_03_map.py:f_03_map \
	-n docker \
	-p test \
	-q docker-deplymet \
  -sb "github/github-prefect-demo" \
  -ib "docker-container/demo-docker-container" \
  -a
"""
from prefect import flow, task

@task
def generate_some_str() -> str:
    return "HELLO"

@task
def do_something(some_str: str) -> list[str]:
    return list(some_str)

@task
def print_something_separately(something: str | list) -> None:
    print("======")
    print(something)
    print("======")

@flow(name="f_03_map")
def f_03_map() -> None:
    some_str = generate_some_str()
    result = do_something(some_str)
    print_something_separately.map(result)

if __name__ == "__main__":
    f_03_map()
