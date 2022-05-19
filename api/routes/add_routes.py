from api.routes import rs_statistics, user


def initialize_routes(app):
    app.include_router(user.router)
    app.include_router(rs_statistics.router)
