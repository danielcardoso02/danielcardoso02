import os
import requests

# Your GitHub username
USERNAME = "danielcardoso02"
# We pull the token securely from your computer's environment variables
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_contribution_data():
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # The GraphQL query to get your exact 365-day grid
    query = """
    query {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                color
		weekday
              }
            }
          }
        }
      }
    }
    """ % USERNAME

    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed: {response.status_code}. {response.text}")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: Please set your GITHUB_TOKEN environment variable in the terminal.")
    else:
        print("Fetching data from GitHub...")
        data = fetch_contribution_data()
        
        # Navigate the JSON response to find the weeks array
        weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
        total_commits = data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
        
        print(f"\n✅ Successfully fetched data for {USERNAME}!")
        print(f"Total commits this year: {total_commits}")
        print(f"Total weeks of data: {len(weeks)}")
        
        print("\nHere is a sample of your earliest week on the graph:")
        for day in weeks[0]['contributionDays']:
            print(f" - Date: {day['date']}, Commits: {day['contributionCount']}, GitHub Color: {day['color']}")
