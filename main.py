import menus
from Auditoria import auth

if __name__ == "__main__":
    if auth.fazer_login():
        menus.menuInicial()
