"""
prefect deployment build \
	src/flow/f_01_quick_start.py:f_01_quick_start \
	-n docker \
	-p test \
	-q docker-deplymet \
  -sb "github/github-prefect-demo" \
  -ib "docker-container/demo-docker-container" \
  -a
"""
import pandas as pd
from prefect import flow, task

@task
def e_data_source_1() -> pd.DataFrame:
    print("Getting df1.")
    return pd.DataFrame(data=[[1], [2]], columns=["col"])

@task
def e_data_source_2() -> pd.DataFrame:
    print("Getting df2.")
    return pd.DataFrame(data=[[3], [4]], columns=["col"])

@task
def t_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    print("Concating df1 and df2.")
    return pd.concat([df1, df2]).reset_index(drop=True)

@task
def l_db1(df: pd.DataFrame) -> None:
    print("Loading df to db1.")
    print(df)
    print("===============")

@task
def l_db2(df: pd.DataFrame) -> None:
    print("Loading df to db2.")
    print(df)
    print("===============")

@flow(name="f_01_quick_start")
def f_01_quick_start() -> None:
    df1 = e_data_source_1()
    df2 = e_data_source_2()
    df = t_concat(df1, df2)
    l_db1(df)
    l_db2(df)

if __name__ == "__main__":
    # f_01_quick_start()
    from prefect.deployments import Deployment
    from prefect_github import GitHubRepository
    from prefect.infrastructure import DockerContainer
    from prefect.filesystems import GitHub

    # storage = GitHubRepository.load("github-prefect-demo")
    # docker_container = DockerContainer.load("demo-docker-container")

    # deployment = Deployment.build_from_flow(
    #     flow=f_01_quick_start,
    #     name="test-deployment",
    #     version="2",
    #     tags=["python-deploy"],
    #     entrypoint="src/flow/f_01_quick_start.py:f_01_quick_start",
    #     storage=storage,
    #     infrastructure=docker_container,
    #     # job_variables=dict("env.PREFECT_LOGGING_LEVEL"="DEBUG"),
    # )
    # deployment.apply()
    # f_01_quick_start.deploy(
    #     name="test-deploy",
    #     work_pool_name="test-docker",
    #     push=False,
    # )

    f_01_quick_start.from_source(
        # source=GitHubRepository.load("github-prefect-demo"),
        source=GitHub.load("github-repo"),
        entrypoint="src/flow/f_01_quick_start.py:f_01_quick_start",
    ).deploy(
        name="test-deploy",
        work_pool_name="test-docker",
        job_variables=dict(pull_policy="Never"),
        # parameters=dict(name="Marvin"),
    )
