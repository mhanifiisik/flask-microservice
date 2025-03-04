from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from loguru import logger
from config import Config

class CouchbaseRepository:
    def __init__(self):
        self._cluster = None
        self._bucket = None
        self._collection = None
        self.connect()

    def connect(self):
        """Establish connection to Couchbase"""
        try:
            self._cluster = Cluster.connect(
                Config.COUCHBASE_HOST,
                ClusterOptions(PasswordAuthenticator(
                    Config.COUCHBASE_USER,
                    Config.COUCHBASE_PASSWORD
                ))
            )
            self._bucket = self._cluster.bucket(Config.COUCHBASE_BUCKET)
            self._collection = self._bucket.default_collection()
            logger.info(f"Connected to Couchbase at {Config.COUCHBASE_HOST}")
        except Exception as e:
            logger.error(f"Failed to connect to Couchbase: {e}")
            raise

    def get_collection(self, scope_name, collection_name):
        """Get a specific collection within a scope"""
        try:
            scope = self._bucket.scope(scope_name)
            return scope.collection(collection_name)
        except Exception as e:
            logger.error(f"Failed to get collection {collection_name} in scope {scope_name}: {e}")
            raise

    def get_default_collection(self):
        """Get the default collection"""
        return self._collection

    def close(self):
        """Close the Couchbase connection"""
        if self._cluster:
            try:
                self._cluster.close()
                logger.info("Couchbase connection closed")
            except Exception as e:
                logger.error(f"Error closing Couchbase connection: {e}") 