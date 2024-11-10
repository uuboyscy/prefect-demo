from prefect import flow


@flow(log_prints=True)
def hello_world_flow(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")

    if goodbye:
        print(f"Goodbye {name}!")


if __name__ == "__main__":
    from prefect_github import GitHubRepository

    hello_world_flow.from_source(
        source=GitHubRepository.load("github-prefect-demo"),
        entrypoint="src/flow/test/hello_world_flow_flow.py:hello_world_flow",
    ).deploy(
        name="test-deploy",
        tags=["test", "project_1"],
        work_pool_name="test-subproc",
        job_variables=dict(pull_policy="Never"),
        # parameters=dict(name="Marvin"),
        cron="1 * * * *"
    )
