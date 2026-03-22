import pandas as pd

from src import settings


def normalize_series(series: pd.Series, reverse: bool = False) -> pd.Series:
    series = pd.to_numeric(series, errors="coerce")

    min_val = series.min()
    max_val = series.max()

    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(0.0, index=series.index)

    if reverse:
        return (max_val - series) / (max_val - min_val)

    return (series - min_val) / (max_val - min_val)


def add_advanced_category_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    score_columns = []

    for category_name, metrics in settings.ADVANCED_STAT_CATEGORIES.items():
        normalized_metric_columns = []

        for metric in metrics:
            if metric not in df.columns:
                continue

            reverse = metric in settings.REVERSED_ADVANCED_STATS
            normalized_col = f"{metric}_norm"

            df[normalized_col] = normalize_series(df[metric], reverse=reverse)
            normalized_metric_columns.append(normalized_col)

        score_col = f"{category_name}_Score"

        if normalized_metric_columns:
            df[score_col] = (
                df[normalized_metric_columns]
                .mean(axis=1)
                .mul(100)
                .round(2)
            )
        else:
            df[score_col] = 0.0

        score_columns.append(score_col)

    if score_columns:
        df["Advanced_Total_Score"] = (
            df[score_columns]
            .mean(axis=1)
            .round(2)
        )
    else:
        df["Advanced_Total_Score"] = 0.0

    return df


def build_advanced_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    tables = {}

    summary_columns = [col for col in settings.ADVANCED_SUMMARY_COLUMNS if col in df.columns]
    tables["Advanced Overview"] = df[summary_columns].copy()

    for category_name, metrics in settings.ADVANCED_STAT_CATEGORIES.items():
        score_col = f"{category_name}_Score"

        table_columns = (
            settings.ADVANCED_BASE_INFO_COLUMNS
            + [score_col]
            + metrics
        )

        table_columns = [col for col in table_columns if col in df.columns]
        tables[category_name] = df[table_columns].copy()

    return tables