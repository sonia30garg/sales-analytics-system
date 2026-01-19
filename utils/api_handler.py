import requests
import os

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  
        data = response.json()

        products = data.get("products", [])

        cleaned = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            }
            for p in products
        ]

        print(f"Successfully fetched {len(cleaned)} products")
        return cleaned

    except Exception as e:
        print(f"Failed to fetch products: {e}")
        return []

import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()   # catches HTTP errors
        data = response.json()

        products = data.get("products", [])

        cleaned = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            }
            for p in products
        ]

        print(f"Successfully fetched {len(cleaned)} products")
        return cleaned

    except Exception as e:
        print(f"Failed to fetch products: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """

    mapping = {}

    for p in api_products:
        pid = p.get("id")
        if pid is None:
            continue  # skip malformed entries

        mapping[pid] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating")
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    """

    enriched = []

    # Ensure output directory exists
    os.makedirs("data", exist_ok=True)
    output_file = "data/enriched_sales_data.txt"

    # Prepare header for output file
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

        for t in transactions:
            try:
                # Extract numeric ID from ProductID (e.g., P101 → 101)
                raw_id = t.get("ProductID", "")
                numeric_id = int(raw_id[1:]) if raw_id[1:].isdigit() else None

                api_info = product_mapping.get(numeric_id)

                if api_info:
                    t["API_Category"] = api_info.get("category")
                    t["API_Brand"] = api_info.get("brand")
                    t["API_Rating"] = api_info.get("rating")
                    t["API_Match"] = True
                else:
                    t["API_Category"] = None
                    t["API_Brand"] = None
                    t["API_Rating"] = None
                    t["API_Match"] = False

                enriched.append(t)

                # Write to file (pipe-delimited)
                row = (
                    f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|"
                    f"{t['ProductName']}|{t['Quantity']}|{t['UnitPrice']}|"
                    f"{t['CustomerID']}|{t['Region']}|"
                    f"{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|"
                    f"{t['API_Match']}\n"
                )
                f.write(row)

            except Exception:
                # Graceful fallback if anything unexpected happens
                t["API_Category"] = None
                t["API_Brand"] = None
                t["API_Rating"] = None
                t["API_Match"] = False
                enriched.append(t)

    print(f"Enriched data saved to {output_file}")
    return enriched


import os

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file in pipe-delimited format.
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Define header
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)

        for t in enriched_transactions:
            # Convert None → empty string for safe writing
            def safe(v):
                return "" if v is None else v

            row = (
                f"{safe(t.get('TransactionID'))}|"
                f"{safe(t.get('Date'))}|"
                f"{safe(t.get('ProductID'))}|"
                f"{safe(t.get('ProductName'))}|"
                f"{safe(t.get('Quantity'))}|"
                f"{safe(t.get('UnitPrice'))}|"
                f"{safe(t.get('CustomerID'))}|"
                f"{safe(t.get('Region'))}|"
                f"{safe(t.get('API_Category'))}|"
                f"{safe(t.get('API_Brand'))}|"
                f"{safe(t.get('API_Rating'))}|"
                f"{safe(t.get('API_Match'))}\n"
            )

            f.write(row)

    print(f"Enriched data saved to {filename}")
