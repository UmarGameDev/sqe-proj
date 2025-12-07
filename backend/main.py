from fastapi import FastAPI

from backend.router import router
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("https://9dc605491367c51c28e8d1acc814867d@o4510492429582336.ingest.us.sentry.io/4510493799809024"),
    send_default_pii=True,
)

app = FastAPI()


@app.get('/')
def get_root():
    return {'message': 'Hello World!'}


app.include_router(router)
