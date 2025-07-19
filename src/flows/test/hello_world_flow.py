"""Quick start."""

from prefect import flow


@flow(log_prints=True)
def hello_world_flow(name: str = "world", goodbye: bool = False) -> None:
    print(f"Hello {name} from Prefect! 🤗")

    if goodbye:
        print(f"Goodbye {name}!")


if __name__ == "__main__":
    """
    Run flow directly, just like Python functions. And the process can also be monitored on UI.
    """
    hello_world_flow()
    # hello_world_flow(name="Ted", goodbye=True)
