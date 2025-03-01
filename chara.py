import csv
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    quote: str

# Define the CSV file name where data will be saved
CSV_FILE = "characters.csv"

# Function to write to CSV
def write_to_csv(name: str, quote: str):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, quote])

# Function to read from CSV
def read_from_csv() -> List[dict]:
    characters = []
    try:
        with open(CSV_FILE, mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                characters.append({"name": row[0], "quote": row[1]})
    except FileNotFoundError:
        pass  # If file doesn't exist yet, just return empty list
    return characters

@app.get("/")
async def welcome():
    return {"Hunter X Hunter": "Characters and Quotes"}

@app.get("/characters")
async def get_charas():
    # Read characters from CSV
    characters = read_from_csv()
    return {"Characters": characters}

@app.get("/characters/{name}")
async def get_chara_by_name(name: str):
    characters = read_from_csv()
    for character in characters:
        if character['name'].lower() == name.lower():
            return {"Character": character}
    raise HTTPException(status_code=404, detail="Character not found")

@app.post("/create_character/")
async def create_chara(chara_data: UserCreate):
    name = chara_data.name
    quote = chara_data.quote
    
    # Write data to CSV
    write_to_csv(name, quote)
    
    return {
        "Message": "Character successfully entered",
        "Name": name,
        "Quote": quote,
    }

@app.get("/quote/")
async def get_quote():
    # Read characters from CSV
    characters = read_from_csv()
    if not characters:
        return {"message": "No characters available"}
    
    # Choose a random character
    character = random.choice(characters)
    return {"character": character}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=1234)
