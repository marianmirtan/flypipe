from datetime import datetime

import pandas as pd
import pytest
from numpy import dtype
from pyspark.sql.types import StringType, DateType

from flypipe.schema import Date
from flypipe.utils import get_schema


@pytest.fixture(scope="function")
def spark():
    from tests.utils.spark import spark

    return spark


@pytest.fixture(scope="function")
def pandas_df():
    return pd.DataFrame(
        data={
            "date": [datetime(2022, 1, 1).date()],
            "date_str": ["31-01-2022"],
        }
    )


@pytest.fixture(scope="function")
def pyspark_df(spark, pandas_df):
    return spark.createDataFrame(pandas_df)


@pytest.fixture(scope="function")
def pandas_on_spark_df(pyspark_df):
    return pyspark_df.to_pandas_on_spark()


class TestDate:
    def test_date(self, pandas_df, pyspark_df, pandas_on_spark_df):
        columns = ["date"]
        type_ = Date()

        df_cast = type_.cast(pandas_df, columns)
        assert {
            "date": dtype("<M8[ns]"),
            "date_str": dtype("O"),
        } == get_schema(df_cast)
        assert df_cast.loc[0, "date"] == datetime(2022, 1, 1).date()

        df_cast = type_.cast(pandas_on_spark_df, columns)
        assert {
            "date": dtype("<M8[ns]"),
            "date_str": dtype("O"),
        } == get_schema(df_cast)
        assert df_cast.loc[0, "date"] == datetime(2022, 1, 1).date()

        df_cast = type_.cast(pyspark_df, columns)
        assert {
            "date": DateType(),
            "date_str": StringType(),
        } == get_schema(df_cast)
        assert df_cast.toPandas().loc[0, "date"] == datetime(2022, 1, 1).date()

    def test_date_str(self, pandas_df, pyspark_df, pandas_on_spark_df):
        columns = ["date_str"]
        type_ = Date(fmt="%d-%m-%Y")

        df_cast = type_.cast(pandas_df, columns)
        assert {
            "date": dtype("O"),
            "date_str": dtype("<M8[ns]"),
        } == get_schema(df_cast)
        assert df_cast.loc[0, "date_str"] == datetime(2022, 1, 31).date()

        df_cast = type_.cast(pandas_on_spark_df, columns)
        assert {
            "date": dtype("O"),
            "date_str": dtype("<M8[ns]"),
        } == get_schema(df_cast)
        assert df_cast.loc[0, "date_str"] == datetime(2022, 1, 31).date()

        type_ = Date(fmt="dd-MM-yyyy")
        df_cast = type_.cast(pyspark_df, columns)

        assert {
            "date": DateType(),
            "date_str": DateType(),
        } == get_schema(df_cast)
        assert df_cast.toPandas().loc[0, "date_str"] == datetime(2022, 1, 31).date()