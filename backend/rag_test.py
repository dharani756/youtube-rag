from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

transcript = api.fetch("jNQXAC9IVRw")

text = " ".join(
    [snippet.text for snippet in transcript]
)

chunk_size = 200

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(
        text[i:i+chunk_size]
    )

print("Chunks:", len(chunks))
print(chunks[0])