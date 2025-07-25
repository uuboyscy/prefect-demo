import pandas as pd
from prefect import flow, task

from utils.prefect_utility import generate_flow_name


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


@flow(name=generate_flow_name())
def f_02_async_task_flow() -> None:
    df1 = e_data_source_1.submit()
    df2 = e_data_source_2.submit()
    df = t_concat.submit(
        df1,
        df2,
        wait_for=[df1, df2],
    )
    l_db1.submit(df, wait_for=[df])
    l_db2.submit(df, wait_for=[df])


if __name__ == "__main__":
    f_02_async_task_flow()
