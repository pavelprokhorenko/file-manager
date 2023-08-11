from src.server import server

app = server.get_app()

if __name__ == "__main__":
    server.serve("src/main:app")
