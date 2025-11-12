"""
Cloudflare R2 Storage Service
Handles file uploads, downloads, and presigned URLs for multi-image uploads and outputs
"""

import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from typing import Optional, List, BinaryIO, Dict, Any
from dataclasses import dataclass
import os
import logging
from datetime import datetime, timedelta
import mimetypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class R2Config:
    """Cloudflare R2 configuration"""
    account_id: str
    access_key_id: str
    secret_access_key: str
    bucket_name: str
    public_url: Optional[str] = None  # Custom domain if configured

class R2StorageService:
    """Service for managing files in Cloudflare R2"""

    def __init__(self, config: R2Config):
        self.config = config
        self.bucket_name = config.bucket_name

        # R2 endpoint URL
        endpoint_url = f"https://{config.account_id}.r2.cloudflarestorage.com"

        # Initialize S3 client for R2
        self.client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
            config=Config(signature_version='s3v4'),
            region_name='auto'  # R2 uses 'auto' region
        )

        logger.info(f"✅ R2 client initialized for bucket: {self.bucket_name}")

    def upload_file(
        self,
        file_path: str,
        object_key: str,
        metadata: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None
    ) -> str:
        """
        Upload a file to R2

        Args:
            file_path: Local path to the file
            object_key: Key (path) in R2 bucket
            metadata: Optional metadata to attach
            content_type: MIME type (auto-detected if not provided)

        Returns:
            Object key of uploaded file
        """
        try:
            # Auto-detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'application/octet-stream'

            extra_args = {
                'ContentType': content_type
            }

            if metadata:
                extra_args['Metadata'] = metadata

            self.client.upload_file(
                file_path,
                self.bucket_name,
                object_key,
                ExtraArgs=extra_args
            )

            logger.info(f"✅ Uploaded: {object_key}")
            return object_key

        except ClientError as e:
            logger.error(f"Failed to upload {object_key}: {e}")
            raise

    def upload_fileobj(
        self,
        file_obj: BinaryIO,
        object_key: str,
        metadata: Optional[Dict[str, str]] = None,
        content_type: str = 'application/octet-stream'
    ) -> str:
        """
        Upload a file object (stream) to R2

        Args:
            file_obj: File-like object
            object_key: Key (path) in R2 bucket
            metadata: Optional metadata
            content_type: MIME type

        Returns:
            Object key of uploaded file
        """
        try:
            extra_args = {
                'ContentType': content_type
            }

            if metadata:
                extra_args['Metadata'] = metadata

            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_key,
                ExtraArgs=extra_args
            )

            logger.info(f"✅ Uploaded stream: {object_key}")
            return object_key

        except ClientError as e:
            logger.error(f"Failed to upload stream {object_key}: {e}")
            raise

    def download_file(self, object_key: str, local_path: str) -> str:
        """
        Download a file from R2

        Args:
            object_key: Key in R2 bucket
            local_path: Where to save locally

        Returns:
            Local file path
        """
        try:
            self.client.download_file(
                self.bucket_name,
                object_key,
                local_path
            )

            logger.info(f"📥 Downloaded: {object_key} -> {local_path}")
            return local_path

        except ClientError as e:
            logger.error(f"Failed to download {object_key}: {e}")
            raise

    def generate_presigned_url(
        self,
        object_key: str,
        expiration: int = 3600,
        method: str = 'get_object'
    ) -> str:
        """
        Generate a presigned URL for temporary access

        Args:
            object_key: Key in R2 bucket
            expiration: URL validity in seconds (default: 1 hour)
            method: 'get_object' for download, 'put_object' for upload

        Returns:
            Presigned URL
        """
        try:
            url = self.client.generate_presigned_url(
                method,
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )

            logger.info(f"🔗 Generated presigned URL for: {object_key} (expires in {expiration}s)")
            return url

        except ClientError as e:
            logger.error(f"Failed to generate presigned URL for {object_key}: {e}")
            raise

    def generate_upload_url(self, object_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for uploading

        Args:
            object_key: Key to upload to
            expiration: URL validity in seconds

        Returns:
            Presigned upload URL
        """
        return self.generate_presigned_url(object_key, expiration, 'put_object')

    def generate_download_url(self, object_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for downloading

        Args:
            object_key: Key to download
            expiration: URL validity in seconds

        Returns:
            Presigned download URL
        """
        return self.generate_presigned_url(object_key, expiration, 'get_object')

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from R2

        Args:
            object_key: Key to delete

        Returns:
            True if successful
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            logger.info(f"🗑️  Deleted: {object_key}")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete {object_key}: {e}")
            raise

    def delete_files(self, object_keys: List[str]) -> Dict[str, Any]:
        """
        Delete multiple files from R2

        Args:
            object_keys: List of keys to delete

        Returns:
            Deletion results
        """
        try:
            objects = [{'Key': key} for key in object_keys]

            response = self.client.delete_objects(
                Bucket=self.bucket_name,
                Delete={'Objects': objects}
            )

            deleted = response.get('Deleted', [])
            errors = response.get('Errors', [])

            logger.info(f"🗑️  Deleted {len(deleted)} files, {len(errors)} errors")

            return {
                'deleted': [obj['Key'] for obj in deleted],
                'errors': errors
            }

        except ClientError as e:
            logger.error(f"Failed to batch delete: {e}")
            raise

    def list_files(self, prefix: str = '', max_keys: int = 1000) -> List[Dict[str, Any]]:
        """
        List files in bucket

        Args:
            prefix: Filter by prefix (folder path)
            max_keys: Maximum number of results

        Returns:
            List of file metadata
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )

            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    'etag': obj['ETag']
                })

            logger.info(f"📂 Listed {len(files)} files with prefix: {prefix}")
            return files

        except ClientError as e:
            logger.error(f"Failed to list files: {e}")
            raise

    def get_file_metadata(self, object_key: str) -> Dict[str, Any]:
        """
        Get metadata for a file

        Args:
            object_key: Key to check

        Returns:
            File metadata
        """
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )

            return {
                'key': object_key,
                'size': response['ContentLength'],
                'content_type': response['ContentType'],
                'last_modified': response['LastModified'],
                'metadata': response.get('Metadata', {}),
                'etag': response['ETag']
            }

        except ClientError as e:
            logger.error(f"Failed to get metadata for {object_key}: {e}")
            raise

    def file_exists(self, object_key: str) -> bool:
        """Check if a file exists in R2"""
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except ClientError:
            return False

    def copy_file(self, source_key: str, dest_key: str) -> str:
        """
        Copy a file within R2

        Args:
            source_key: Source file key
            dest_key: Destination file key

        Returns:
            Destination key
        """
        try:
            copy_source = {
                'Bucket': self.bucket_name,
                'Key': source_key
            }

            self.client.copy_object(
                CopySource=copy_source,
                Bucket=self.bucket_name,
                Key=dest_key
            )

            logger.info(f"📋 Copied: {source_key} -> {dest_key}")
            return dest_key

        except ClientError as e:
            logger.error(f"Failed to copy {source_key} to {dest_key}: {e}")
            raise


class ProjectFileManager:
    """High-level file manager for R&D platform projects"""

    def __init__(self, r2_service: R2StorageService):
        self.r2 = r2_service

    def _get_project_path(self, user_id: str, project_id: str, job_id: str) -> str:
        """Generate consistent path structure"""
        return f"users/{user_id}/projects/{project_id}/jobs/{job_id}"

    def upload_scan_images(
        self,
        user_id: str,
        project_id: str,
        job_id: str,
        image_files: List[tuple]  # [(filename, file_obj), ...]
    ) -> Dict[str, Any]:
        """
        Upload multiple scan images for a job

        Args:
            user_id: User ID
            project_id: Project ID
            job_id: Processing job ID
            image_files: List of (filename, file_object) tuples

        Returns:
            Upload results with presigned URLs
        """
        base_path = self._get_project_path(user_id, project_id, job_id)
        uploaded = []

        for i, (filename, file_obj) in enumerate(image_files):
            object_key = f"{base_path}/input/images/{i:03d}_{filename}"

            try:
                self.r2.upload_fileobj(
                    file_obj,
                    object_key,
                    metadata={
                        'user_id': user_id,
                        'project_id': project_id,
                        'job_id': job_id,
                        'image_index': str(i)
                    },
                    content_type='image/jpeg'
                )

                uploaded.append({
                    'index': i,
                    'filename': filename,
                    'key': object_key,
                    'status': 'success'
                })

            except Exception as e:
                uploaded.append({
                    'index': i,
                    'filename': filename,
                    'status': 'failed',
                    'error': str(e)
                })

        return {
            'uploaded': len([u for u in uploaded if u['status'] == 'success']),
            'failed': len([u for u in uploaded if u['status'] == 'failed']),
            'files': uploaded,
            'input_path': f"{base_path}/input/images/"
        }

    def upload_output_files(
        self,
        user_id: str,
        project_id: str,
        job_id: str,
        step_file: Optional[str] = None,
        stl_file: Optional[str] = None,
        preview_image: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Upload processing output files

        Returns:
            Dict with presigned download URLs
        """
        base_path = self._get_project_path(user_id, project_id, job_id)
        urls = {}

        if step_file:
            key = f"{base_path}/output/model.step"
            self.r2.upload_file(step_file, key, content_type='application/step')
            urls['step_url'] = self.r2.generate_download_url(key, expiration=86400)  # 24 hours

        if stl_file:
            key = f"{base_path}/output/model.stl"
            self.r2.upload_file(stl_file, key, content_type='model/stl')
            urls['stl_url'] = self.r2.generate_download_url(key, expiration=86400)

        if preview_image:
            key = f"{base_path}/output/preview.png"
            self.r2.upload_file(preview_image, key, content_type='image/png')
            urls['preview_url'] = self.r2.generate_download_url(key, expiration=86400)

        return urls

    def generate_upload_urls(
        self,
        user_id: str,
        project_id: str,
        job_id: str,
        image_count: int
    ) -> List[Dict[str, str]]:
        """
        Generate presigned upload URLs for direct client uploads

        Args:
            user_id: User ID
            project_id: Project ID
            job_id: Job ID
            image_count: Number of images to upload

        Returns:
            List of upload URLs with metadata
        """
        base_path = self._get_project_path(user_id, project_id, job_id)
        upload_urls = []

        for i in range(image_count):
            object_key = f"{base_path}/input/images/{i:03d}.jpg"
            url = self.r2.generate_upload_url(object_key, expiration=3600)

            upload_urls.append({
                'index': i,
                'upload_url': url,
                'key': object_key
            })

        return upload_urls

    def cleanup_job_files(self, user_id: str, project_id: str, job_id: str) -> Dict[str, Any]:
        """Delete all files for a job"""
        base_path = self._get_project_path(user_id, project_id, job_id)
        files = self.r2.list_files(prefix=base_path)
        keys = [f['key'] for f in files]

        if keys:
            return self.r2.delete_files(keys)

        return {'deleted': [], 'errors': []}


# ============================================================================
# INITIALIZATION
# ============================================================================

def create_r2_service() -> R2StorageService:
    """Create R2 service from environment variables"""
    config = R2Config(
        account_id=os.getenv('R2_ACCOUNT_ID', ''),
        access_key_id=os.getenv('R2_ACCESS_KEY_ID', ''),
        secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY', ''),
        bucket_name=os.getenv('R2_BUCKET_NAME', 'rd-platform'),
        public_url=os.getenv('R2_PUBLIC_URL')
    )
    return R2StorageService(config)


if __name__ == "__main__":
    # Example usage
    r2 = create_r2_service()
    manager = ProjectFileManager(r2)

    # Generate upload URLs for client
    urls = manager.generate_upload_urls(
        user_id="user-123",
        project_id="proj-456",
        job_id="job-789",
        image_count=25
    )

    print(f"Generated {len(urls)} upload URLs")
