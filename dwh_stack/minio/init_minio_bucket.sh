#!/bin/sh
set -e

MAX_RETRIES=10
RETRY_INTERVAL=5

echo "Configuring MinIO client..."
/usr/bin/mc alias set local "${MINIO_HOST}" "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}" || {
    echo "ERROR: Failed to set alias for MinIO"
    exit 1
}

# Check if MinIO is ready
for i in $(seq 1 "${MAX_RETRIES}"); do
    if /usr/bin/mc admin info local &>/dev/null; then
        echo 'MinIO is ready!'
        break
    fi
    
    echo "MinIO not ready, waiting ${RETRY_INTERVAL} seconds... (Attempt ${i}/${MAX_RETRIES})"
    sleep "${RETRY_INTERVAL}"

    if [ "${i}" -eq "${MAX_RETRIES}" ]; then
        echo "ERROR: MinIO did not become ready after ${MAX_RETRIES} attempts. Check if the service is running and accessible."
        exit 1
    fi
done

# Create the bucket if it does not exist
/usr/bin/mc mb --ignore-existing local/"${BUCKET_NAME}" || {
    echo "ERROR: Failed to create bucket ${BUCKET_NAME}"
    exit 1
}
echo "Bucket ${BUCKET_NAME} created or already exists."

# Set public access for the bucket
/usr/bin/mc anonymous set public local/"${BUCKET_NAME}" || {
    echo "ERROR: Failed to set public access for bucket ${BUCKET_NAME}"
    exit 1
}
echo "Public access for bucket ${BUCKET_NAME} has been set."

echo "All operations with MinIO completed successfully."