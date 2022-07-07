import update_json
import os

def get_user():
    user = os.system("whoami")
    print("whoami= " , user)

def main():
    update_json.update("configs/fig6.json","cloud_user", get_user() )

if __name__ == "__main__":
    print("Setting config...")
    main()

# Maybe pipe whoami in as an arugment??? . whoami = 0 is what is currently happening when python runs it