# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from pathlib import Path
from typing import Optional

from google.adk.artifacts.file_artifact_service import FileArtifactService


class GlobalFileArtifactService(FileArtifactService):
    """
    A file-backed artifact service that ignores user isolation,
    making all artifacts global.
    """

    def _base_root(self, user_id: str, /) -> Path:
        """Returns the global artifacts root directory, ignoring user_id."""
        return self.root_dir / "global"

    def _scope_root(
        self,
        user_id: str,
        session_id: Optional[str],
        filename: str,
    ) -> Path:
        """Returns the global artifacts directory, ignoring session_id."""
        # We want everything in 'global/artifacts' regardless of session or user
        return self._base_root(user_id) / "artifacts"
