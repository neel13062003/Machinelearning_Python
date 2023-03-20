# # this will work only when youtube video have subtitles
#
# from sklearn.feature_extraction.text import CountVectorizer
# import re
# from youtube_transcript_api import YouTubeTranscriptApi as yta
#
# #url, descriptio, title i will get from webapp
#
# # https://www.youtube.com/watch?v=w82a1FT5o88
# # https://www.youtube.com/watch?v=OIIg5d_WSMc
# # https://www.youtube.com/watch?v=y0aqyspGsdA
# # https://www.youtube.com/watch?v=S7xTBa93TX8
# # https://www.youtube.com/watch?v=Bf-dbS9CcRU      microsoft
# # https://www.youtube.com/watch?v=ebls5x-gb0s      microsoft
# # https://www.youtube.com/watch?v=-glZip6foVk      microsoft
# vid_id = 'Bf-dbS9CcRU'
# vid_id2 = 'ebls5x-gb0s'
#
# # extract text
# data = yta.get_transcript(vid_id)
#
# # array
# outls = []
#
# # our logic to transcribe better
# transcript = ''
# for value in data:
#     for key, val in value.items():
#         if key == 'text':
#             transcript += val + ' '  # Add a space between each text segment
#             outls.append(val)  # Append each text segment to the list for vectorization
#
# # write out transcript to file
# with open("neel.txt", 'w') as f:
#     f.write(transcript)
#
#
# # title,discription
# # Get the title and description of the video
# title = "The Future of Work With AI - Microsoft March 2023 Event"  # Replace with actual title of the video
# description = "A special event with Satya Nadella and Jared Spataro focused on how AI will power a whole new way of working for everyone. Introducing Microsoft 365 Copilot Copilot in Microsoft 365 Apps20:29 - The Copilot System 23:01 - Copilot in Teams and Business Process28:57 - Introducing Business Chat33:36 - Microsoft's Approach to Responsible AI "
#
# title2 = "Introducing Microsoft 365 Copilot with Outlook, PowerPoint, Excel, and OneNote"
# description2 = "Planning a grad party? Microsoft 365 Copilot has you covered. Learn how Microsoft 365 Copilot seamlessly integrates into the apps you use every day to turn your words into the most powerful productivity tool on the planet.Check out these highlights from the March, 16 2023 event"
#
# # Replace with actual description of the video
#
# # Combine the title and description into a single string
# title_desc = title + ' ' +description
# title_desc2 = title2 + ' ' +description2
#
#
# vectorizer = CountVectorizer()
# vectorizer.fit(outls)
#
#
#
# # Vectorize the title and description
# title_desc_vec = vectorizer.transform([title_desc])
#
# # Vectorize the title2 and description2
# title_desc_vec2 = vectorizer.transform([title_desc2])
#
#
# # Get the feature names from the vectorizer
# feature_names = vectorizer.get_feature_names_out()
#
#
#
# # printing unique words
# print("Vocabulary:", vectorizer.get_feature_names_out())
#
#
# # Count the number of words in the title and description that are also present in the transcript
# count = 0
# for word in feature_names:
#     if title_desc_vec[0, vectorizer.vocabulary_.get(word)] > 0:
#         count += 1
#
#
# # Count the number of words in the title2 and description2 that are also present in the transcript
# count2 = 0
# for word in feature_names:
#     if title_desc_vec2[0, vectorizer.vocabulary_.get(word)] > 0:
#         count2 += 1
#
#
# # Print the count of matching words
# print("Number of matching words:", count)
#
# # Print the count of matching words for title2 and description2
# print("Number of matching words for title2 and description2:", count2)

from sklearn.feature_extraction.text import CountVectorizer
from youtube_transcript_api import YouTubeTranscriptApi as yta

# Define the list of video IDs with their titles and descriptions

videos = [
    # {'id': 'w82a1FT5o88', 'title': 'Video 1 Title', 'description': 'Video 1 Description'},
    {'id': '-glZip6foVk ', 'title': 'Streamline business processes with Microsoft 365 Copilot', 'description': 'When you lead a sales team, building customer relationships and closing deals are key. Microsoft 365 Copilot can help lighten the load with next-generation AI. Learn how Microsoft 365 Copilot works across Teams, Viva Sales, and Power Automate to streamline business processes.'},
    {'id': 'Bf-dbS9CcRU', 'title': 'The Future of Work With AI - Microsoft March 2023 Event',
     'description': 'A special event with Satya Nadella and Jared Spataro focused on how AI will power a whole new way of working for everyone. Introducing Microsoft 365 Copilot Copilot in Microsoft 365 Apps20:29 - The Copilot System 23:01 - Copilot in Teams and Business Process28:57 - Introducing Business Chat33:36 - Microsoft\'s Approach to Responsible AI'},
    {'id': 'ebls5x-gb0s', 'title': 'Introducing Microsoft 365 Copilot with Outlook, PowerPoint, Excel, and OneNote',
     'description': 'Planning a grad party? Microsoft 365 Copilot has you covered. Learn how Microsoft 365 Copilot seamlessly integrates into the apps you use every day to turn your words into the most powerful productivity tool on the planet.Check out these highlights from the March, 16 2023 event'},
]

# Initialize the list to store the counts of matching words for each video
counts = []

# Extract text from transcript of each video and vectorize it
for video in videos:
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

# Get the indices of the videos with the top 3 counts
top_counts_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)[:3]

# Print the top 3 videos
print("Top 3 videos:")

# print(type(video))

# url = "https://www.youtube.com/watch?v"+id

for index in top_counts_indices[:3]:
    video = videos[index]
    id = video['id']
    url = "https://www.youtube.com/watch?v=" + id
    # print(video['id'], video['title'], video['description'])
    print(video['title'],url)
