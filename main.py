from app import create_app
from routers import auth, logs

app = create_app()

app.include_router(auth.router)
app.include_router(logs.router)
