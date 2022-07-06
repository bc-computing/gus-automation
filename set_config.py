import update_json
import os

def get_user():
    return os.run("whoami")

def main():
    update_json.update("configs/fig6.json","cloud_user",get_user() )

if __name__ == "__main__":
    main()

