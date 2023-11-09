from help import grab_next_data as next_data
import json

segments = next_data("https://www.stedi.com/edi/x12-004010/segment")
SEGMENT_BASE_URL = "https://stedi.com/edi" + segments["page"].replace(
    "[release]", segments["props"]["pageProps"]["release"]
)
segments = segments["props"]["pageProps"]["segments"]
segments_filtered = []
for i in range(len(segments)):
    url = SEGMENT_BASE_URL + "/" + segments[i]["id"]
    segments[i]["url"] = url
    print(f"Getting details for segment {segments[i]['id']} from {url}")
    segment_details = next_data(url)
    if not segment_details["props"]["pageProps"]["segmentInRelease"]:
        continue
    segments[i]["desc"] = segment_details["props"]["pageProps"]["seg"]["purpose"]
    segments[i]["elements"] = segment_details["props"]["pageProps"]["seg"]["elements"]
    segments[i]["appearsIn"] = segment_details["props"]["pageProps"][
        "appearsInTransactions"
    ]
    segments_filtered.append(segments[i])

with open("Segments.json", "w") as f:
    f.write(json.dumps(segments_filtered))
