import boto3
from botocore.exceptions import ClientError
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for interacting with S3/MinIO."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the S3 bucket exists."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Create bucket
                try:
                    if settings.AWS_REGION == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION}
                        )
                    logger.info(f"Created S3 bucket: {self.bucket_name}")
                except ClientError as create_error:
                    logger.error(f"Failed to create bucket: {str(create_error)}")
                    raise
    
    async def upload_file(
        self,
        file_content: bytes,
        key: str,
        content_type: Optional[str] = None
    ) -> str:
        """Upload file to S3."""
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_content,
                **extra_args
            )
            
            logger.info(f"Uploaded file to S3: {key}")
            return key
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise
    
    async def download_file(self, key: str) -> bytes:
        """Download file from S3."""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return response['Body'].read()
            
        except ClientError as e:
            logger.error(f"S3 download failed: {str(e)}")
            raise
    
    async def delete_file(self, key: str):
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            logger.info(f"Deleted file from S3: {key}")
            
        except ClientError as e:
            logger.error(f"S3 delete failed: {str(e)}")
            raise
    
    def generate_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for file access."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return url
            
        except ClientError as e:
            logger.error(f"Presigned URL generation failed: {str(e)}")
            raise


# Singleton instance
s3_service = S3Service()