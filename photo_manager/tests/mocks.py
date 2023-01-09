"""Mocks for a tests."""


class UUIDMock:
    """UUID module Mock."""

    @property
    def hex(self):
        """Hex mock."""
        return 'hex'


def uuid4_mock(*args, **kwargs):
    """UUID4 Mock."""
    return UUIDMock()


class S3ClientMock:
    """S3 Client Mock."""

    def upload_file(*args, **kwargs):
        """Upload File Mock."""
        return None


def boto3_client_mock(*args, **kwargs):
    """Boto3 Client Mock."""
    return S3ClientMock
