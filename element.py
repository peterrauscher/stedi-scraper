from help import grab_next_data as next_data
import json

elements = next_data("https://www.stedi.com/edi/x12-004010/element")
TRANS_BASE_URL = "https://stedi.com/edi" + elements["page"].replace(
    "[release]", elements["props"]["pageProps"]["release"]
)
elements = elements["props"]["pageProps"]["elements"]
composites = elements["props"]["pageProps"]["composites"]
elements_filtered = []
composites_filtered = []

for i in range(len(elements)):
    url = TRANS_BASE_URL + "/" + elements[i]["id"]
    elements[i]["url"] = url
    element_details = next_data(url)
    if not element_details["props"]["pageProps"]["elementInRelease"]:
        continue
    elements[i]["desc"] = element_details["props"]["pageProps"]["elt"]["definition"]
    elements[i]["dataType"] = element_details["props"]["pageProps"]["elt"][
        "data_element_type"
    ]
    if "maximum_length" in element_details["props"]["pageProps"]["elt"]:
        elements[i]["maxLength"] = element_details["props"]["pageProps"]["elt"][
            "maximum_length"
        ]
    if "minimum_length" in element_details["props"]["pageProps"]["elt"]:
        elements[i]["minLength"] = element_details["props"]["pageProps"]["elt"][
            "minimum_length"
        ]
    if "codes" in element_details["props"]["pageProps"]["elt"]:
        elements[i]["codes"] = element_details["props"]["pageProps"]["elt"]["codes"]
    elements[i]["appearsIn"] = element_details["props"]["pageProps"][
        "appearsInSegments"
    ]
    elements_filtered.append(elements[i])

for i in range(len(composites)):
    url = TRANS_BASE_URL + "/" + composites[i]["id"]
    composites[i]["url"] = url
    composite_details = next_data(url)
    if not composite_details["props"]["pageProps"]["elementInRelease"]:
        continue
    composites[i]["desc"] = composite_details["props"]["pageProps"]["elt"]["purpose"]
    if "elements" in composite_details["props"]["pageProps"]["elt"]:
        composites[i]["codes"] = composite_details["props"]["pageProps"]["elt"][
            "elements"
        ]
    composites[i]["appearsIn"] = composite_details["props"]["pageProps"][
        "appearsInSegments"
    ]
    composites_filtered.append(composites[i])


with open("Elements.json", "w") as f:
    f.write(
        json.dumps({"elements": elements_filtered, "composites": composites_filtered})
    )
