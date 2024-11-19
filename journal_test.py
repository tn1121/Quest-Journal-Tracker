import requests

URL = "http://127.0.0.1:8000/journal/entries/"


# Sample Data
sample_data1 = {
        "character_ID": 1,
        "entry_text": "Sample Text 1",
        "entry_date": "2010-10-01",
        "campaign_ID": 1
    }
sample_data2 = {
        "character_ID": 2,
        "entry_text": "Sample Text 2",
        "entry_date": "2009-01-30",
        "campaign_ID": 1
    }
sample_data3 = {
        "character_ID": 3,
        "entry_text": "Sample Text 3",
        "entry_date": "2014-11-21",
        "campaign_ID": 3
    }
sample_data4 = {
        "character_ID": 1,
        "entry_text": "Sample Text 4",
        "entry_date": "2013-01-14",
        "campaign_ID": 1
    }
# Create a new entry
def test_create_entry(entry_data):
    response = requests.post(URL, json=entry_data)
    print("CREATE Response:", response.json())
    return response.json()

# Read new entry data
def test_read_entry(character_ID):
    response = requests.get(f"{URL}{character_ID}")
    print("READ Response:", response.json())

# View shared entry progress across campaign
def test_read_campaign_ID(campaign_ID):
    response = requests.get(f"{"http://127.0.0.1:8000"}{"/campaign/journal/"}{campaign_ID}")
    print("READ Response:", response.json())

if __name__ == "__main__":
    # Add Journal Entry
    test_create_entry(sample_data1)
    test_create_entry(sample_data2)
    test_create_entry(sample_data3)
    test_create_entry(sample_data4)

    # Retrieve Journal Entry
    test_read_entry(1)

    # Access collective campaign journal
    test_read_campaign_ID(1)


