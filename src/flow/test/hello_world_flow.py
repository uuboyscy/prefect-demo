from prefect import flow


@flow(log_prints=True)
def hello_world(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")

    if goodbye:
        print(f"Goodbye {name}!")


if __name__ == "__main__":

    # 本來只有這樣寫
    # hello_world(goodbye=True)

    # # 現在要測試可以這樣寫
    # hello_world.serve(name="my-first-deployment",
    #                   tags=["onboarding"],
    #                   parameters={"goodbye": True},
    #                   interval=60)

    # hello_world.deploy(
    #     name="test-deployment",
    #     # image="uuboyscy/docker-tutorial",
    #     work_pool_name="test-docker",
    # )

    from prefect.deployments import Deployment
    from prefect_github import GitHubRepository

    storage = GitHubRepository.load("github-prefect-demo")

    deployment = Deployment.build_from_flow(
        flow=hello_world,
        name="test-deployment",
        version="2",
        tags=["python-deploy"],
        storage=storage,
        # job_variables=dict("env.PREFECT_LOGGING_LEVEL"="DEBUG"),
    )
    deployment.apply()