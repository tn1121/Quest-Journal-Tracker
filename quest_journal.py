from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated, Union
from datetime import date

# ---------------------------------------------------------
# Quest database model
# ---------------------------------------------------------

# Create database model
class QuestBase(SQLModel):
    title: str = Field(index=True)
    objectives: str
    rewards: str
    status: str = Field(index=True, default="Incomplete")
    campaign_ID: int | None = Field(default=None, index=True)

class Quest(QuestBase, table=True):
    quest_ID: int | None = Field(default=None, primary_key=True)

# Create data model for updating quest
class QuestUpdate(QuestBase):
    title: Union[str, None] = None
    objectives: Union[str, None] = None
    rewards: Union[str, None] = None
    status: Union[str, None] = None
    campaign_ID: Union[int, None] = None

# ---------------------------------------------------------
# Journal Entry database model
# ---------------------------------------------------------

# Create database model
class EntryBase(SQLModel):
    character_ID: int | None = Field(default=None, index=True)
    entry_text: str
    entry_date: date = Field(default_factory=date.today)
    campaign_ID: int | None = Field(default=None, index=True)
    

class Entry(EntryBase, table=True):
    entry_ID: int | None = Field(default=None, primary_key=True)

# Create data model for updating journal entry
class EntryUpdate(EntryBase):
    character_ID: Union[int, None] = None
    entry_text: Union[str, None] = None
    entry_date: Union[date, None] = None
    campaign_ID: Union[int, None] = None

# Create SQLModel 
sqlite_file_name = "quest_journal_db.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Create table models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create session dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# Create database when app starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ---------------------------------------------------------
# Quest Entry Routes
# ---------------------------------------------------------

# Create Quest
@app.post("/quests/")
def create_quest(quest: Quest, session: SessionDep):
    db_quest = Quest.model_validate(quest)
    session.add(db_quest)
    session.commit()
    session.refresh(db_quest)
    return {"Quest Status": "Quest created successfully."}

# Get all quest data
@app.get("/quests/", response_model=list[Quest])
def get_all_quests(
    session: SessionDep,
):
    quests = session.exec(select(Quest)).all()
    if not quests:
        raise HTTPException(status_code=404, detail="No quests were found.")
    return quests

# Get Quest data
@app.get("/quests/{quest_ID}")
def get_quest(quest_ID: int, session: SessionDep) -> Quest:
    quest = session.get(Quest, quest_ID)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest ID not found.")
    return quest

# Delete Quest
@app.delete("/quests/{quest_ID}")
def delete_quest(quest_ID: int, session: SessionDep):
    quest = session.get(Quest, quest_ID)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest ID not found.")
    session.delete(quest)
    session.commit()
    return {"Quest Status": "Quest deleted successfully."}

# Update Quest
@app.patch("/quests/{quest_ID}")
def update_quest(quest_ID: int, quest: QuestUpdate, session: SessionDep):
    quest_db = session.get(Quest, quest_ID)
    if not quest_db:
        raise HTTPException(status_code=404, detail="Quest ID not found.")
    quest_data = quest.model_dump(exclude_unset=True)
    quest_db.sqlmodel_update(quest_data)
    session.add(quest_db)
    session.commit()
    session.refresh(quest_db)
    return {"Quest Status": "Quest updated successfully."}

# View Shared Quest Progress
@app.get("/quests/progress/{campaign_ID}", response_model=list[Quest])
def get_campaign_quests(campaign_ID: int, session: SessionDep):
    quests = session.exec(select(Quest).where(Quest.campaign_ID == campaign_ID)).all()
    if not quests:
        raise HTTPException(status_code=404, detail="No quests found for the given campaign ID.")
    return quests


# ---------------------------------------------------------
# Journal Entry Routes
# ---------------------------------------------------------

# Create Journal Entry
@app.post("/journal/entries/")
def create_entry(entry: Entry, session: SessionDep):
    db_entry = Entry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return {"Journal Entry Status": "Entry created successfully."}

# Get all journal entry data
@app.get("/journal/entries/", response_model=list[Entry])
def get_all_entries(
    session: SessionDep,
):
    entries = session.exec(select(Entry)).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries were found.")
    return entries

# Get journal entry data
@app.get("/journal/{entry_ID}")
def get_entry(entry_ID: int, session: SessionDep) -> Entry:
    entry = session.get(Entry, entry_ID)
    if not entry:
        raise HTTPException(status_code=404, detail="Journal Entry ID not found.")
    return entry

# Delete journal entry
@app.delete("/journal/entries/{entry_ID}")
def delete_entry(entry_ID: int, session: SessionDep):
    entry = session.get(Entry, entry_ID)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry ID not found.")
    session.delete(entry)
    session.commit()
    return {"Journal Entry Status": "Journal Entry deleted successfully."}

# Update Journal Entry
@app.patch("/journal/entries/{entry_ID}")
def update_entry(entry_ID: int, entry: EntryUpdate, session: SessionDep):
    entry_db = session.get(Entry, entry_ID)
    if not entry_db:
        raise HTTPException(status_code=404, detail="Journal Entry ID not found.")
    entry_data = entry.model_dump(exclude_unset=True)
    entry_db.sqlmodel_update(entry_data)
    session.add(entry_db)
    session.commit()
    session.refresh(entry_db)
    return {"Journal Entry Status": "Journal entry updated successfully."}

# View character journal
@app.get("/journal/entries/{character_ID}", response_model=list[Entry])
def get_character_journal(character_ID: int, session: SessionDep):
    entries = session.exec(select(Entry).where(Entry.character_ID == character_ID).order_by(Entry.entry_date)).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No journal entries found for that character.")
    return entries

# Access collective campaign journal
@app.get("/campaign/journal/{campaign_ID}", response_model=list[Entry])
def get_campaign_journal(campaign_ID: int, session: SessionDep):
    entries = session.exec(select(Entry).where(Entry.campaign_ID == campaign_ID).order_by(Entry.entry_date)).all()
    if not entries:
        raise HTTPException(status_code=404, detail="No journal entries found for that campaign.")
    return entries