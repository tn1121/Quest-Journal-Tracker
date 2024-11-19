# Overview
This application uses FastAPI to manage quests and journal entries in an SQLite database. It supports functionality for creating, reading, updating, and deleting quests and journal entries, allowing for users to easily track quest/journal data for campaigns. 

# Requirements
FastAPI

SQLModel 

typing

datetime

requests

Uvicorn

SQLite


# Request Data
A. To request data, HTTP methods such as GET, POST, PATCH, or DELETE will work. This can be done in python by installing the requests library. Data is retrieved using query paramaters, such as campaign_ID and character_ID. 
EXAMPLE: Create a new quest request
def test_create_quest(quest_data):
    response = requests.post(URL, json=quest_data)
    print("CREATE Response:", response.json())
    return response.json()
    
# Receive Data
B. To recieve data, HTTP methods will also work, with the response being in JSON format. When creating or updating quests or journal entries, the data must use a specific format that follows the database models. 
EXAMPLE: Receiving POST request to create a new quest 
@app.post("/quests/")
def create_quest(quest: Quest, session: SessionDep):
    db_quest = Quest.model_validate(quest)
    session.add(db_quest)
    session.commit()
    session.refresh(db_quest)
    return {"Quest Status": "Quest created successfully."}
# UML Diagram
C.![uml](https://github.com/user-attachments/assets/bab8f160-6911-47bc-85dd-2bdb36d39382)
ts/c9db4006-d5f7-4e39-a3c4-f5f973546627)
1. Client sends HTTP request to the API
2. API calls get_session() function to obtain a database session
3. The session uses session.get() to query the database
4. The database returns the data with the associated quest ID
5. The session passes the data to the API
6. The API froms a JSON response and sends to the client.

