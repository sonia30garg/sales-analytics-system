def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.

    Returns: list of raw lines (strings)
    """

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']

    for enc in encodings_to_try:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
            break  # Successfully read the file, exit loop
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except UnicodeDecodeError:
            # Try next encoding
            continue

    # If all encodings failed
    if not lines:
        print("Error: Unable to decode file with supported encodings.")
        return []

    # Strip whitespace, skip header, remove empty lines
    cleaned = [
        line.strip()
        for line in lines[1:]  # skip header row
        if line.strip()        # remove empty lines
    ]

    return cleaned


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """

    parsed = []
    expected_fields = 8

    for line in raw_lines:
        parts = line.split("|")

        # Skip malformed rows
        if len(parts) != expected_fields:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Clean product name (remove commas inside names)
        product_name = product_name.replace(",", " ")

        # Clean numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        # Convert types safely
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip rows with invalid numeric values
            continue

        parsed.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    return parsed


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    """

    required_fields = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    valid = []
    invalid_count = 0

    # --- VALIDATION PHASE ---
    for t in transactions:
        # Check required fields exist and are non-empty
        if any(f not in t or t[f] in (None, "") for f in required_fields):
            invalid_count += 1
            continue

        # Validate ID formats
        if not t['TransactionID'].startswith("T"):
            invalid_count += 1
            continue
        if not t['ProductID'].startswith("P"):
            invalid_count += 1
            continue
        if not t['CustomerID'].startswith("C"):
            invalid_count += 1
            continue

        # Validate numeric rules
        if t['Quantity'] <= 0:
            invalid_count += 1
            continue
        if t['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        valid.append(t)

    # --- FILTERING PHASE ---
    total_input = len(transactions)

    # Show available regions
    regions_available = sorted({t['Region'] for t in valid})
    print("Available regions:", regions_available)

    # Show transaction amount range
    amounts = [t['Quantity'] * t['UnitPrice'] for t in valid]
    if amounts:
        print(f"Transaction amount range: min={min(amounts)}, max={max(amounts)}")

    # Filter by region
    filtered_by_region = 0
    if region:
        before = len(valid)
        valid = [t for t in valid if t['Region'] == region]
        filtered_by_region = before - len(valid)
        print(f"After region filter ({region}): {len(valid)} records")

    # Filter by amount
    filtered_by_amount = 0
    if min_amount is not None or max_amount is not None:
        before = len(valid)
        def amount_ok(t):
            amt = t['Quantity'] * t['UnitPrice']
            if min_amount is not None and amt < min_amount:
                return False
            if max_amount is not None and amt > max_amount:
                return False
            return True

        valid = [t for t in valid if amount_ok(t)]
        filtered_by_amount = before - len(valid)
        print(f"After amount filter: {len(valid)} records")

    # Final summary
    summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid)
    }

    return valid, invalid_count, summary


# Step 1: Read raw lines from the file
raw_lines = read_sales_data("sales_data.txt")

# Step 2: Parse the cleaned transactions
transactions = parse_transactions(raw_lines)

# Step 3: Use the parsed data
print(f"Loaded {len(transactions)} valid transactions")
for t in transactions[:5]:   # show first 5
    print(t)

valid, invalid_count, summary = validate_and_filter(
    transactions
    region="South",
    min_amount=2000
)
