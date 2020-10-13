import os
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

class DBConnection:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'claver'
        self.connection = mysql.connector.connect(host=self.host,
                                                  user=self.user,
                                                  password=self.password,
                                                  database=self.database)

    def get_prepared_cursor(self):
        return self.connection.cursor(prepared=True)

    def commit(self):
        self.connection.commit()

    def cleanup(self):
        self.connection.close()

    def update_seed(self, id, seed):
        stmt = "UPDATE node_devices SET seed = ? WHERE id = ?"
        query = self.get_prepared_cursor()
        try:
            status = query.execute(stmt, (seed, id,))
            self.commit()
            print(status)
        except Error as e:
            print("Error with query")
            # print(e)
        finally:
            query.close()
            self.cleanup()

class SyncKey:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.db_connector = DBConnection()
        self.run()

    def getSecretKey(self):
        with open(self.dir_path + "/secret_inSecureStorage.txt", "r") as file:
            for line in file:
                secret_key = line.strip()
        return secret_key

    def savePublicKey(self, key):
        with open(self.dir_path + "/public_inSecureStorage.txt", "w") as file:
            file.write(key)

    def run(self):
        secret_key = self.getSecretKey().encode()
        new_public_key = Fernet.generate_key()      # Rotate the public key
        reencrypted_key = Fernet(new_public_key).encrypt(secret_key)

        print(f"Public key: {new_public_key}")
        print(f"Encrypted public key: {reencrypted_key}")

        self.savePublicKey(new_public_key.decode())
        self.db_connector.update_seed(2, reencrypted_key)

if __name__ == "__main__":
    SyncKey()