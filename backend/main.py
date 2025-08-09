from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from chains import run_image_story_graph
from contextlib import asynccontextmanager

TEMP_DIR = Path("temp_images")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic: clear temp_images folder
    if TEMP_DIR.exists():
        for item in TEMP_DIR.iterdir():
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Failed to delete {item}. Reason: {e}")
    yield

app = FastAPI(lifespan=lifespan)

# CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_story/")
async def generate_story(
    image: UploadFile,
    user_input: str = Form(...),
    genre: str = Form(...)
):
    TEMP_DIR.mkdir(exist_ok=True)

    temp_filename = TEMP_DIR / f"{uuid.uuid4().hex}_{image.filename}"
    with temp_filename.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = run_image_story_graph(
        image_path=str(temp_filename),
        user_input=user_input,
        genre=genre
    )

    return JSONResponse({
        "image_caption": result["image_caption"],
        "story": result["story"],
        "reflection": result["reflection"]
    })
