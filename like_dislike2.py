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

# rating
scores = []

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

        # Get the video statistics
        url = "https://www.googleapis.com/youtube/v3/videos?id=" + video[
            'id'] + "&part=statistics&key=AIzaSyCQlCzFJXXTpljhHn5fYfNxY3Ypt9mBvhg"

        response = requests.get(url)
        statistics = json.loads(response.text)['items'][0]['statistics']
        view_count = int(statistics['viewCount'])
        like_count = int(statistics['likeCount'])
        # dislike_count = int(statistics['dislikeCount'])
        comment_count = int(statistics['commentCount'])

        # only check how much likecount,dislike count
        # print("neel")
        # print(like_count)
        #print(dislike_count)
        # print(comment_count)

        # Calculate the score
        vectorizer = CountVectorizer()
        vectorizer.fit([transcript_text, title_desc])
        transcript_vec = vectorizer.transform([transcript_text])
        title_desc_vec = vectorizer.transform([title_desc])
        feature_names = vectorizer.get_feature_names_out()
        count = 0
        for word in feature_names:
            if title_desc_vec[0, vectorizer.vocabulary_.get(word)] > 0:
                count += transcript_vec[0, vectorizer.vocabulary_.get(word)]
        # score = (view_count * 0.4) + (like_count * 0.3) - (dislike_count * 0.2) + (comment_count * 0.1) + count
        score = (view_count * 0.4) + (like_count * 0.3) + (comment_count * 0.1) + count
        scores.append(score)
    except:
        # print("kalp")
        # If the transcript data is not available, skip the video
        scores.append(0)

# Get the indices of the videos with the top 3 counts
# top_counts_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)[:3]
top_scores_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]



# Create a dictionary to store the data
data = {"top_videos": []}

# Add the top 3 videos to the dictionary
# for index in top_counts_indices[:3]:
for index in top_scores_indices[:1]:
    video = videos[index]
    id = video['id']
    url = "https://www.youtube.com/watch?v=" + id
    title = video['title']
    data["top_videos"].append({"title": title, "url": url})


# Convert the dictionary to JSON
json_data = json.dumps(data)
print(json_data)

