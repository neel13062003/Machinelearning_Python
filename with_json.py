import json
import requests
from sklearn.feature_extraction.text import CountVectorizer
from youtube_transcript_api import YouTubeTranscriptApi as yta

# Define the list of video IDs with their titles and descriptions

videos = [
    # {'id': 'w82a1FT5o88', 'title': 'Video 1 Title', 'description': 'Video 1 Description'},
    {'id': '-glZip6foVk', 'title': 'Streamline business processes with Microsoft 365 Copilot', 'description': 'When you lead a sales team, building customer relationships and closing deals are key. Microsoft 365 Copilot can help lighten the load with next-generation AI. Learn how Microsoft 365 Copilot works across Teams, Viva Sales, and Power Automate to streamline business processes.'},
    {'id': 'Bf-dbS9CcRU', 'title': 'The Future of Work With AI - Microsoft March 2023 Event',
     'description': 'A special event with Satya Nadella and Jared Spataro focused on how AI will power a whole new way of working for everyone. Introducing Microsoft 365 Copilot Copilot in Microsoft 365 Apps20:29 - The Copilot System 23:01 - Copilot in Teams and Business Process28:57 - Introducing Business Chat33:36 - Microsoft\'s Approach to Responsible AI'},
    {'id': 'ebls5x-gb0s', 'title': 'Introducing Microsoft 365 Copilot with Outlook, PowerPoint, Excel, and OneNote',
     'description': 'Planning a grad party? Microsoft 365 Copilot has you covered. Learn how Microsoft 365 Copilot seamlessly integrates into the apps you use every day to turn your words into the most powerful productivity tool on the planet.Check out these highlights from the March, 16 2023 event'},
    {'id': '6mbwJ2xhgzM&list=PLu0W_9lII9agiCUZYRsvtGTXdxkzPyItg',
     'title': 'Introduction to HTML, CSS, JavaScript & How websites work? | Web Development',
     'description': 'This video is a part of this Complete Web Development in Hindi Course Playlist'},
    {'id': 'TUbWFRiHn0Y', 'title': 'Great Legend Ronaldo by Unstoppable Motivation',
     'description': 'He has a huge fan following, but very few people know about the struggle behind his success and his dedication level for football. In this video, I have briefed a few incidents of Great Legend Ronaldo which shows his dedication level.'},
]

# Initialize the list to store the counts of matching words for each video
counts = []

# Extract text from transcript of each video and vectorize it
for video in videos:
    try:
        # Get the transcript text
        transcript_data = yta.get_transcript(video['id'])
        transcript_text = ' '.join([value['text'] for value in transcript_data])

        # Combine the title and description into a single string
        title_desc = video['title'] + ' ' + video['description']

        # Vectorize the transcript and title+description
        vectorizer = CountVectorizer()
        vectorizer.fit([transcript_text, title_desc])
        transcript_vec = vectorizer.transform([transcript_text])
        title_desc_vec = vectorizer.transform([title_desc])

        # Count the number of matching words
        feature_names = vectorizer.get_feature_names_out()
        count = 0
        for word in feature_names:
            if title_desc_vec[0, vectorizer.vocabulary_.get(word)] > 0:
                count += transcript_vec[0, vectorizer.vocabulary_.get(word)]
        counts.append(count)
    except:
        # If the transcript data is not available, skip the video
        counts.append(0)

# Get the indices of the videos with the top 3 counts
top_counts_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)[:3]

# Create a dictionary to store the data
data = {"top_videos": []}

# Add the top 3 videos to the dictionary
for index in top_counts_indices:
    video = videos[index]
    id = video['id']
    url = "https://www.youtube.com/watch?v=" + id
    title = video['title']
    data["top_videos"].append({"title": title, "url": url})


# Convert the dictionary to JSON
json_data = json.dumps(data)
print(json_data)

# # Send the JSON data to Node.js using a POST request
# url = "http://localhost:3000/"
# headers = {"Content-Type": "application/json"}
# response = requests.post(url, headers=headers, data=json_data)

# # Print the response from Node.js
# print(response.text)

