from mycards.app import app
from mycards import routes

# Debug print a list of available routes pathnames and methods
for route in app.url_map.iter_rules():
    print(f"{route.endpoint}: {route.rule} ({', '.join(route.methods)})")

if __name__ == '__main__':
    app.run()