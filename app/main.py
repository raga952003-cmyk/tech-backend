from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, learning_paths, quizzes, progress, interviews
import os

app = FastAPI(
    title="TechStudy Tracker API",
    description="Personalized Learning Journey for IT Professionals",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Start email scheduler on startup (optional - requires apscheduler)
@app.on_event("startup")
async def startup_event():
    try:
        from app.services.scheduler_service import start_scheduler
        start_scheduler()
    except ImportError:
        print("Scheduler not available - install apscheduler to enable email notifications")

# Stop scheduler on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    try:
        from app.services.scheduler_service import stop_scheduler
        stop_scheduler()
    except ImportError:
        pass

# CORS configuration - Professional setup with environment variable support
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
origins = [origin.strip() for origin in cors_origins.split(",")]

# Add common development origins
default_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]

# Combine and deduplicate origins
all_origins = list(set(origins + default_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
print(f"Auth router routes: {[r.path for r in auth.router.routes]}")
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(learning_paths.router, prefix="/api/learning-paths", tags=["Learning Paths"])
app.include_router(quizzes.router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["AI Interviews"])

@app.get("/")
def read_root():
    return {
        "message": "TechStudy Tracker API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TechStudy Tracker API"}
