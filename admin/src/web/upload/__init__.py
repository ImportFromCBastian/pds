from minio import Minio


class Storage:
    def __init__(self, app=None):
        self._client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the storage client with the app configuration.
        """
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)
        self._client = Minio(
            minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        app.storage = self

        return app

    @property
    def client(self):
        """
        Get the storage client.
        """
        return self._client

    @client.setter
    def client(self, value):
        """
        Set the storage client.
        """
        self._client = value


storage = Storage()
