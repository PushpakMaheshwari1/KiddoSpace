from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.auth import auth_router
from api.project import router as project_router
from api.streak import router as streak_router
from api.achievements import router as achievement_router
import requests

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NASA_API_KEY = "iLdJbFQSrR12tyhEEMeV3T1yDzDhOcF83Us119LE"

@app.get("/apod/")
def get_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        specific_data = {
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation"),
            "date": data.get("date"),
        }
        return specific_data
    raise HTTPException(status_code=500, detail="Error fetching APOD data")


# Endpoint to get Mars Rover Photos
@app.get("/mars-rover-photos/")
def get_mars_rover_photos():
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        photos = data.get("camera", [])
        specific_data = [
            {
                "img_src": photo.get("img_src"),
                "earth_date": photo.get("earth_date"),
                "rover_name": photo["rover"]["name"] if "rover" in photo else None
            }
            for photo in photos
        ]
        return specific_data
    raise HTTPException(status_code=500, detail="Error fetching Mars Rover data")


# Endpoint to get Near-Earth Object (NEO) data
@app.get("/neo/")
def get_neo_data():
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        neos = data.get("near_earth_objects", [])
        specific_data = [
            {
                "id": neo.get("id"),
                "name": neo.get("name"),
                "absolute_magnitude_h": neo.get("absolute_magnitude_h"),
                "estimated_diameter_kilometers": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                if "estimated_diameter" in neo else None
            }
            for neo in neos
        ]
        return specific_data
    raise HTTPException(status_code=500, detail="Error fetching NEO data")

# Include the authentication router
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(streak_router)
app.include_router(achievement_router)