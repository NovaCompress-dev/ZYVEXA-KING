import hashlib
import os
import pickle

class ZyvexaEngine:
    def __init__(self, vault_name="zyvexa_vault.dat", index_name="zyvexa_index.db"):
        self.vault_name = vault_name
        self.index_name = index_name
        self.chunk_size = 4096 
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_name):
            try:
                with open(self.index_name, 'rb') as f:
                    return pickle.load(f)
            except:
                return {}
        return {}

    def _save_index(self):
        with open(self.index_name, 'wb') as f:
            pickle.dump(self.index, f)

    def process_data(self, file_path):
        recipe = []
        with open(file_path, 'rb') as f, open(self.vault_name, 'ab+') as vault:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk: 
                    break
                
                c_hash = hashlib.sha256(chunk).hexdigest()
                
                if c_hash not in self.index:
                    offset = vault.tell()
                    vault.write(chunk)
                    self.index[c_hash] = (offset, len(chunk))
                
                recipe.append(c_hash)
        
        self._save_index()
        return recipe
