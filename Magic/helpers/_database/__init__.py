
import ast
import os
import sys

import config
from Magic.helpers._load import HOSTED_ON


Redis = MongoDB = None
if config.REDIS_URI:
    try:
        from redis import Redis
    except ImportError:
        os.system("pip3 install -q redis hiredis")
        from redis import Redis
elif config.MONGO_URL:
    try:
        from pymongo import MongoClient as MongoDB
    except ImportError:
        os.system("pip3 install -q pymongo[srv]")
        from pymongo import MongoClient


class Database:
    def __init__(self, *args, **kwargs):
        self._cache = {}

    def get_key(self, key):
        if key in self._cache:
            return self._cache[key]
        value = self._get_data(key)
        self._cache.update({key: value})
        return value

    def re_cache(self):
        self._cache.clear()
        for key in self.keys():
            self._cache.update({key: self.get_key(key)})

    def ping(self):
        return 1

    @property
    def usage(self):
        return 0

    def keys(self):
        return []

    def del_key(self, key):
        if key in self._cache:
            del self._cache[key]
        self.delete(key)
        return True

    def _get_data(self, key=None, data=None):
        if key:
            data = self.get(str(key))
        if data:
            try:
                data = ast.literal_eval(data)
            except BaseException:
                pass
        return data

    def set_key(self, key, value):
        value = self._get_data(data=value)
        self._cache[key] = value
        return self.set(str(key), str(value))

    def rename(self, key1, key2):
        _ = self.get_key(key1)
        if _:
            self.del_key(key1)
            self.set_key(key2, _)
            return 0
        return 1


class DBMongo(Database):
    def __init__(self, key, dbname="DBMagic"):
        self.dB = MongoDB(key, serverSelectionTimeoutMS=5000)
        self.db = self.dB[dbname]
        super().__init__()

    def __repr__(self):
        return f"<Magic.DBMongo\n -total_keys: {len(self.keys())}\n>"

    @property
    def name(self):
        return "Mongo"

    @property
    def usage(self):
        return self.db.command("dbstats")["dataSize"]

    def ping(self):
        if self.dB.server_info():
            return True

    def keys(self):
        return self.db.list_collection_names()

    def set_key(self, key, value):
        if key in self.keys():
            self.db[key].replace_one({"_id": key}, {"value": str(value)})
        else:
            self.db[key].insert_one({"_id": key, "value": str(value)})
        self._cache.update({key: value})
        return True

    def delete(self, key):
        self.db.drop_collection(key)

    def get(self, key):
        if x := self.db[key].find_one({"_id": key}):
            return x["value"]

    def flushall(self):
        self.dB.drop_database("DBMagic")
        self._cache.clear()
        return True
        
        
class DBRedis(Database):
    def __init__(
        self,
        host,
        port,
        password,
        platform="",
        *args,
        **kwargs,
    ):
        if host and ":" in host:
            spli_ = host.split(":")
            host = spli_[0]
            port = int(spli_[-1])
            if host.startswith("http"):
                print("REDIS_URI tidak perlu menggunakan https://")
                import sys

                sys.exit()
        elif not host or not port:
            print("Port tidak ditemukan.")
            import sys

            sys.exit()
        kwargs["host"] = host
        kwargs["password"] = password
        kwargs["port"] = port

        if not host:
            var, hash_, host, password = "", "", "", ""
            for vars_ in os.environ:
                if vars_.startswith("QOVERY_REDIS_") and vars.endswith("_HOST"):
                    var = vars_
            if var:
                hash_ = var.split("_", maxsplit=2)[1].split("_")[0]
            if hash:
                kwargs["host"] = os.environ.get(f"QOVERY_REDIS_{hash_}_HOST")
                kwargs["port"] = os.environ.get(f"QOVERY_REDIS_{hash_}_PORT")
                kwargs["password"] = os.environ.get(f"QOVERY_REDIS_{hash_}_PASSWORD")
        self.db = Redis(**kwargs)
        self.set = self.db.set
        self.get = self.db.get
        self.keys = self.db.keys
        self.delete = self.db.delete
        super().__init__()

    @property
    def name(self):
        return "Redis"

    @property
    def usage(self):
        return sum(self.db.memory_usage(x) for x in self.keys())
        
def DBMagic():
    try:
        if Redis:
            return DBRedis(
                host=config.REDIS_URI,
                password=config.REDIS_PASSWORD,
                platform=HOSTED_ON,
                port=config.REDISPORT,
                decode_responses=True,
                socket_timeout=5,
                retry_on_timeout=True,
            )
        if MongoDB:
            return DBMongo(config.MONGO_URL)
    except BaseException as e:
        print(f"ERROR: {e}")
    
    
MDB = DBMagic()
