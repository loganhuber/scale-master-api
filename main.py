from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import user, score

# Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  # Default Create React App port
    "http://localhost:5173",  # Default Vite port
    "http://127.0.0.1:5173",
    "https://loganhuber.github.io",
    "https://scale-master.xyz",
    "https://www.scale-master.xyz" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific client applications
    allow_credentials=True,           # Allows cookies and auth headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all request headers
)

app.include_router(user.router, prefix='/api/users', tags=['users'])
app.include_router(score.router, prefix='/api/scores', tags=['scores'])

