import pandas as pd
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

@flow(name="f_04_forloop_submit")
def f_04_forloop_submit() -> None:
    some_str = generate_some_str()
    result = do_something(some_str)
    for each_str in result:
        print_something_separately.submit(each_str)

if __name__ == "__main__":
    f_04_forloop_submit()
