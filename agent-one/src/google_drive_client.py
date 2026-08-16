"""Google Drive API Client for Agent One"""

import json
import logging
from typing import List, Optional, Tuple, Dict
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io

from config.constants import GOOGLE_DRIVE_OAUTH_JSON


class GoogleDriveClient:
    """Handles all Google Drive API operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Drive API using service account"""
        if not GOOGLE_DRIVE_OAUTH_JSON:
            self.logger.warning(
                "GOOGLE_DRIVE_OAUTH_JSON not set. Some operations may fail."
            )
            return

        try:
            # Parse service account JSON
            service_account_info = json.loads(GOOGLE_DRIVE_OAUTH_JSON)

            # Create credentials
            credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=["https://www.googleapis.com/auth/drive"],
            )

            # Build Drive service
            self.service = build("drive", "v3", credentials=credentials)
            self.logger.info("✅ Authenticated with Google Drive API")
        except Exception as e:
            self.logger.error(f"Failed to authenticate with Google Drive: {e}")
            raise

    def list_files_in_folder(
        self, folder_id: str, file_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """List files in a folder (optionally filtered by type)"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return []

        try:
            query = f"'{folder_id}' in parents and trashed=false"

            if file_types:
                type_conditions = " or ".join(
                    [f"mimeType='{mime}'" for mime in file_types]
                )
                query += f" and ({type_conditions})"

            results = (
                self.service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="files(id, name, mimeType, createdTime, modifiedTime)",
                    pageSize=100,
                )
                .execute()
            )

            files = results.get("files", [])
            self.logger.info(f"Found {len(files)} files in folder {folder_id}")
            return files

        except Exception as e:
            self.logger.error(f"Error listing files: {e}")
            return []

    def find_video_and_brief(self, folder_id: str) -> List[Tuple[Dict, Optional[Dict]]]:
        """Find video files and their accompanying brief files in a folder"""
        if not self.service:
            return []

        try:
            # Video MIME types
            video_mimes = [
                "video/mp4",
                "video/quicktime",
                "video/x-msvideo",
                "video/x-matroska",
            ]

            video_files = self.list_files_in_folder(folder_id, video_mimes)

            video_brief_pairs = []

            for video in video_files:
                # Look for accompanying brief file
                video_base_name = video["name"].rsplit(".", 1)[0]
                brief_name = f"{video_base_name}_brief.txt"

                brief = self._find_file_by_name(folder_id, brief_name)

                video_brief_pairs.append((video, brief))

            return video_brief_pairs

        except Exception as e:
            self.logger.error(f"Error finding video and brief pairs: {e}")
            return []

    def _find_file_by_name(self, folder_id: str, file_name: str) -> Optional[Dict]:
        """Find a specific file by name in a folder"""
        if not self.service:
            return None

        try:
            query = f"'{folder_id}' in parents and name='{file_name}' and trashed=false"

            results = (
                self.service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="files(id, name, mimeType)",
                    pageSize=1,
                )
                .execute()
            )

            files = results.get("files", [])
            return files[0] if files else None

        except Exception as e:
            self.logger.error(f"Error finding file {file_name}: {e}")
            return None

    def download_file(self, file_id: str, output_path: Path) -> bool:
        """Download a file from Google Drive"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return False

        try:
            request = self.service.files().get_media(fileId=file_id)
            file_handler = io.FileIO(output_path, "wb")
            downloader = MediaIoBaseDownload(file_handler, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            file_handler.close()
            self.logger.info(f"✅ Downloaded file to {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error downloading file {file_id}: {e}")
            return False

    def upload_file(
        self, local_path: Path, folder_id: str, file_name: str
    ) -> Optional[str]:
        """Upload a file to Google Drive"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return None

        try:
            file_metadata = {"name": file_name, "parents": [folder_id]}

            media = MediaFileUpload(local_path, resumable=True)

            file = (
                self.service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )

            self.logger.info(f"✅ Uploaded {file_name} (ID: {file['id']})")
            return file["id"]

        except Exception as e:
            self.logger.error(f"Error uploading file {local_path}: {e}")
            return None

    def create_folder(self, folder_name: str, parent_folder_id: str) -> Optional[str]:
        """Create a folder in Google Drive"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return None

        try:
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_folder_id],
            }

            folder = self.service.files().create(body=file_metadata, fields="id").execute()

            self.logger.info(f"✅ Created folder {folder_name} (ID: {folder['id']})")
            return folder["id"]

        except Exception as e:
            self.logger.error(f"Error creating folder: {e}")
            return None

    def move_file(self, file_id: str, new_folder_id: str) -> bool:
        """Move a file to a different folder"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return False

        try:
            # Get current parents
            file = self.service.files().get(fileId=file_id, fields="parents").execute()
            previous_parents = ",".join(file.get("parents", []))

            # Move to new folder
            self.service.files().update(
                fileId=file_id,
                addParents=new_folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            ).execute()

            self.logger.info(f"✅ Moved file {file_id} to folder {new_folder_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error moving file: {e}")
            return False

    def delete_file(self, file_id: str) -> bool:
        """Delete a file from Google Drive"""
        if not self.service:
            self.logger.error("Not authenticated with Google Drive")
            return False

        try:
            self.service.files().delete(fileId=file_id).execute()
            self.logger.info(f"✅ Deleted file {file_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            return False
