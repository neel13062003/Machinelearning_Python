from pytube import YouTube

link = "https://youtu.be/Jxd63PGOlYE?list=PLauivoElc3girg6gOwzd1f8BQlnfjOM6P"
youtube_1 = YouTube(link)

videos = youtube_1.streams.all()

for i, video in enumerate(videos):
    print(f"{i}: {video}")

stream_number = int(input("Enter the stream number to download: "))
selected_video = videos[stream_number]
selected_video.download()
print("Video downloaded successfully!")


# from pytube import YouTube
#
# link = "https://youtu.be/Jxd63PGOlYE?list=PLauivoElc3girg6gOwzd1f8BQlnfjOM6P"
# youtube_1 = YouTube(link)
#
# #youtube function
# # print(youtube_1.title)
# # print(youtube_1.thumbnail_url)
#
# videos = youtube_1.streams.all()
# #all streams qualitya valible i get
# #videos= youtube_1.streams.filter(only_audio=True)
#
# #through enumerate i can get index
# vid = list(enumerate(videos))
# for i in vid:
#     print(i)
# print()
# strm = int(input("enter:"))
# videos[strm].download()
# print('Successfully')

#Playlist function
# from pytube import Playlist
# py = Playlist("https://www.youtube.com/playlist?list=PLauivoElc3girg6gOwzd1f8BQlnfjOM6P")
# print(f'Downloading:{py.title}')
# for video in py.videos:
#     video.streams.first().download()
# print('Successfully')