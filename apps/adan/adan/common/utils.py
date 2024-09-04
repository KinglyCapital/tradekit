from fastapi.responses import JSONResponse
from pandas import DataFrame
from pandas.api.types import is_datetime64_any_dtype  # type: ignore


def to_response(df: DataFrame) -> JSONResponse:
    data = df.to_dict(orient="records")  # type: ignore
    return JSONResponse(content=data)


def format_datetime(df: DataFrame):
    for column in df.columns:
        if is_datetime64_any_dtype(df[column]):
            df[column] = df[column].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df
