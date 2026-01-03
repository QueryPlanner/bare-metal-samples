from pathlib import Path
from urllib.parse import unquote, urlparse

from google.adk.cli.service_registry import get_service_registry

from platform_utils.global_artifact_service import GlobalFileArtifactService


def global_file_artifact_factory(uri: str, **kwargs):
    parsed_uri = urlparse(uri)
    if parsed_uri.netloc not in ("", "localhost"):
        raise ValueError("globalfile:// artifact URIs must reference the local filesystem.")
    if not parsed_uri.path:
        raise ValueError("globalfile:// artifact URIs must include a path component.")
    artifact_path = Path(unquote(parsed_uri.path))
    return GlobalFileArtifactService(root_dir=artifact_path)

get_service_registry().register_artifact_service("globalfile", global_file_artifact_factory)
