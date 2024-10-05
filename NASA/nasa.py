from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

NASA_API_KEY = "YOUR_NASA_API_KEY"

@app.get("/apod/")
def get_apod():
    """Get Astronomy Picture of the Day with specific data"""
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        # Extract specific data
        data = response.json()
        specific_data = {
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation"),
            "date": data.get("date"),
        }
        return specific_data
    raise HTTPException(status_code=500, detail="Error fetching APOD data")

@app.get("/mars-rover-photos/")
def get_mars_rover_photos():
    """Get specific data from Mars Rover Photos"""
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        photos = data.get("photos", [])
        # Extract specific fields from each photo
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

@app.get("/neo/")
def get_neo_data():
    """Get specific data from Near-Earth Objects API"""
    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={NASA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        neos = data.get("near_earth_objects", [])
        # Extract specific fields from each NEO object
        specific_data = [
            {
                "id": neo.get("id"),
                "name": neo.get("name"),
                "absolute_magnitude_h": neo.get("absolute_magnitude_h"),
                "estimated_diameter_kilometers": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"] if "estimated_diameter" in neo else None
            }
            for neo in neos
        ]
        return specific_data
    raise HTTPException(status_code=500, detail="Error fetching NEO data")
