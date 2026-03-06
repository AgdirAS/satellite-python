import boto3
from os import environ as env


S3 = boto3.resource("s3")
S3_CLIENT = boto3.client("s3")
OUTPUT_BUCKET = env.get("S3_BUCKET", "spatial-production")
S3_BUCKET = S3.Bucket(OUTPUT_BUCKET)
