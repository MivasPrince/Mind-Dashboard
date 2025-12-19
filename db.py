"""db.py

BigQuery-only database access layer for the MIND Unified Dashboard.

Security goals
1) Read-only by design: this module refuses to execute non-SELECT queries.
2) No credentials are hard-coded in this repo.

Authentication options (choose one)
- Streamlit secrets: add a [bigquery] section and a service account JSON under
  [gcp_service_account] in .streamlit/secrets.toml.
- Environment variables: set GOOGLE_APPLICATION_CREDENTIALS to point to a
  service account JSON file.

Required secrets
- project_id
- dataset
- location (optional)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Optional

import pandas as pd


_READ_ONLY_OK_RE = re.compile(r"^\s*(?:--.*\n\s*)*(WITH\b|SELECT\b)", re.IGNORECASE)


@dataclass(frozen=True)
class BigQueryConfig:
    project_id: str
    dataset: str
    location: Optional[str] = None

    def table(self, name: str) -> str:
        """Return a fully-qualified BigQuery table reference."""
        return f"`{self.project_id}.{self.dataset}.{name}`"


class ReadOnlyQueryError(ValueError):
    pass


class BigQueryManager:
    """Thin BigQuery wrapper returning pandas DataFrames."""

    def __init__(self, config: BigQueryConfig, credentials: Any = None):
        # Lazy import to keep local/dev environments friendly.
        from google.cloud import bigquery  # type: ignore

        self._bigquery = bigquery
        self.config = config
        self.client = bigquery.Client(
            project=config.project_id,
            credentials=credentials,
            location=config.location,
        )

    @staticmethod
    def _assert_read_only(query: str) -> None:
        """Reject any query that isn't SELECT/WITH."""
        if not _READ_ONLY_OK_RE.search(query):
            raise ReadOnlyQueryError(
                "Read-only mode: only SELECT/WITH queries are allowed. "
                "Refusing to run potentially mutating SQL."
            )

    def query_df(self, query: str, params: Optional[Mapping[str, Any]] = None) -> pd.DataFrame:
        """Execute a read-only query and return a DataFrame."""
        self._assert_read_only(query)

        job_config = self._bigquery.QueryJobConfig()
        if params:
            job_config.query_parameters = [
                self._bigquery.ScalarQueryParameter(k, None, v) for k, v in params.items()
            ]

        job = self.client.query(query, job_config=job_config)
        return job.result().to_dataframe(create_bqstorage_client=True)


def _load_bq_config_from_streamlit() -> Optional[BigQueryConfig]:
    """Load BigQuery config from Streamlit secrets if available."""
    try:
        import streamlit as st

        if "bigquery" not in st.secrets:
            return None
        bq = st.secrets["bigquery"]
        return BigQueryConfig(
            project_id=str(bq.get("project_id", "")).strip(),
            dataset=str(bq.get("dataset", "")).strip(),
            location=str(bq.get("location", "")).strip() or None,
        )
    except Exception:
        return None


def _load_credentials_from_streamlit():
    """Load service account credentials from Streamlit secrets if present."""
    try:
        import streamlit as st
        from google.oauth2 import service_account  # type: ignore

        if "gcp_service_account" not in st.secrets:
            return None

        info = dict(st.secrets["gcp_service_account"])  # secrets is mapping-like
        # NOTE: Do not log/print this.
        return service_account.Credentials.from_service_account_info(info)
    except Exception:
        return None


_CACHED_MANAGER: Optional[BigQueryManager] = None


def get_db_manager() -> BigQueryManager:
    """Singleton BigQuery manager.

    The dashboard expects this function name.
    """
    global _CACHED_MANAGER
    if _CACHED_MANAGER is not None:
        return _CACHED_MANAGER

    # Prefer Streamlit secrets when present.
    cfg = _load_bq_config_from_streamlit()
    if cfg and cfg.project_id and cfg.dataset:
        creds = _load_credentials_from_streamlit()
        _CACHED_MANAGER = BigQueryManager(cfg, credentials=creds)
        return _CACHED_MANAGER

    # Fallback to environment variables.
    import os

    project_id = os.getenv("BQ_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT") or ""
    dataset = os.getenv("BQ_DATASET") or "mind_analytics"
    location = os.getenv("BQ_LOCATION")

    if not project_id:
        raise RuntimeError(
            "BigQuery is not configured. Set Streamlit secrets [bigquery]project_id, "
            "or set the BQ_PROJECT_ID/GOOGLE_CLOUD_PROJECT environment variable."
        )

    cfg = BigQueryConfig(project_id=project_id, dataset=dataset, location=location)
    _CACHED_MANAGER = BigQueryManager(cfg)
    return _CACHED_MANAGER


def init_database() -> None:
    """Backward-compatible init hook.

    Older versions of this repo initialized a Postgres schema at runtime.
    For BigQuery (read-only), we only validate connectivity.
    """
    _ = get_db_manager()
