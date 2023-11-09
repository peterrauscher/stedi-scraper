from help import grab_next_data as next_data
import json

transactions = next_data("https://www.stedi.com/edi/x12-004010/transaction-set")
TRANS_BASE_URL = "https://stedi.com/edi" + transactions["page"].replace(
    "[release]", transactions["props"]["pageProps"]["release"]
)
transactions = transactions["props"]["pageProps"]["sets"]
transactions_filtered = []

for i in range(len(transactions)):
    url = TRANS_BASE_URL.replace("transaction-set", transactions[i]["id"])
    transactions[i]["url"] = url
    print(f"Getting details for transaction {transactions[i]["id"]} from {url}")
    transaction_details = next_data(url)
    if not transaction_details["props"]["pageProps"]["setInRelease"]:
        continue
    transactions[i]["desc"] = transaction_details["props"]["pageProps"]["transaction"][
        "purpose"
    ]
    transactions[i]["heading"] = transaction_details["props"]["pageProps"][
        "transaction"
    ]["heading"]
    transactions[i]["detail"] = transaction_details["props"]["pageProps"][
        "transaction"
    ]["detail"]
    transactions[i]["summary"] = transaction_details["props"]["pageProps"][
        "transaction"
    ]["summary"]
    transactions[i]["functionalGroupId"] = transaction_details["props"]["pageProps"]["transaction"][
        "functional_group_id"
    ]
    transactions_filtered.append(transactions[i])

with open("Transactions.json", "w") as f:
    f.write(json.dumps(transactions_filtered))
