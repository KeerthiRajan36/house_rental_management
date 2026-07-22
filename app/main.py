from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import Base
from app.database.database import engine

from app.routers.auth import router as auth_router
from app.routers.houses import router as house_router
from app.routers.tenants import router as tenant_router
from app.routers.payments import router as payment_router
from app.routers.reports import router as report_router

from app.exceptions.handlers import register_exception_handlers



Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="House Rental & Tenant Management API"
)



register_exception_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)

app.include_router(house_router)

app.include_router(tenant_router)

app.include_router(payment_router)

app.include_router(report_router)



@app.get("/")
def root():

    return {
        "message": "House Rental & Tenant Management API",
    }
