from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title=f" Batch Test API",
        version="0.0.1",
        redoc_url=None,
    )

    @app.get(f"/status", tags=["Status"])
    def health_check():
        return dict(
            status="OK",
        )

    return app
