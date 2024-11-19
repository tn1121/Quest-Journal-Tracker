import requests

URL = "http://127.0.0.1:8000/quests/"


# Sample Data
sample_data1 = {
        "title": "Save the cat!",
        "objectives": "Rescue the cat from the tree.",
        "rewards": "5 gold coins",
        "status": "Incomplete",
        "campaign_ID": 1
    }
sample_data2 = {
        "title": "Feed a dog.",
        "objectives": "Give the dog some meat.",
        "rewards": "3 gold coins",
        "status": "Complete",
        "campaign_ID": 1
    }
sample_data3 = {
        "title": "Slay the Dragon!",
        "objectives": "Kill the dragon.",
        "rewards": "500 gold coins",
        "status": "Incomplete",
        "campaign_ID": 2
    }
# Create a new quest
def test_create_quest(quest_data):
    response = requests.post(URL, json=quest_data)
    print("CREATE Response:", response.json())
    return response.json()

# Update the quest
def test_update_quest(quest_ID):
    update_data = {
        "rewards": "500 gold coins",
        "status": "Complete"
    }
    response = requests.patch(f"{URL}{quest_ID}", json=update_data)
    print("UPDATE Response:", response.json())

# Read new quest data
def test_read_quest(quest_ID):
    response = requests.get(f"{URL}{quest_ID}")
    print("READ Response:", response.json())

# View shared quest progress across campaign
def test_read_campaign_ID(campaign_ID):
    response = requests.get(f"{URL}{"progress/"}{campaign_ID}")
    print("READ Response:", response.json())

# Delete a quest
def test_delete_quest(quest_ID):
    response = requests.delete(f"{URL}{quest_ID}")
    print("DELETE Response:", response.json())

if __name__ == "__main__":
    # Create Quest
    test_create_quest(sample_data1)
    test_create_quest(sample_data2)
    test_create_quest(sample_data3)

    # Read quest using quest ID
    test_read_quest(1)
    test_read_quest(2)
    test_read_quest(3)

    # Update created quest
    test_update_quest(1)
    test_read_quest(1)

    # View shared quests by campaign ID
    test_read_campaign_ID(1)

    # Delete quest
    test_delete_quest(3)
    test_read_quest(3)


