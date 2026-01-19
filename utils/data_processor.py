def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    """
    total = 0.0

    for t in transactions:
        total += t['Quantity'] * t['UnitPrice']

    return total


def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    """

    region_stats = {}

    # --- Aggregate totals per region ---
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    # --- Compute overall total for percentage calculation ---
    overall_total = sum(r['total_sales'] for r in region_stats.values())

    # --- Add percentage field ---
    for region, stats in region_stats.items():
        if overall_total > 0:
            stats['percentage'] = round((stats['total_sales'] / overall_total) * 100, 2)
        else:
            stats['percentage'] = 0.0

    # --- Sort by total_sales descending ---
    region_stats = dict(
        sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
    )

    return region_stats


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    """

    product_stats = {}

    # --- Aggregate totals per product ---
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if name not in product_stats:
            product_stats[name] = {
                'total_qty': 0,
                'total_revenue': 0.0
            }

        product_stats[name]['total_qty'] += qty
        product_stats[name]['total_revenue'] += revenue

    # --- Convert to list of tuples ---
    results = [
        (name, stats['total_qty'], stats['total_revenue'])
        for name, stats in product_stats.items()
    ]

    # --- Sort by total quantity sold (descending) ---
    results.sort(key=lambda x: x[1], reverse=True)

    # --- Return top n ---
    return results[:n]



def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    """

    customer_stats = {}

    # --- Aggregate per customer ---
    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']

        if cid not in customer_stats:
            customer_stats[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()   # use set for uniqueness
            }

        customer_stats[cid]['total_spent'] += amount
        customer_stats[cid]['purchase_count'] += 1
        customer_stats[cid]['products_bought'].add(product)

    # --- Compute averages and convert sets to lists ---
    for cid, stats in customer_stats.items():
        if stats['purchase_count'] > 0:
            stats['avg_order_value'] = round(
                stats['total_spent'] / stats['purchase_count'], 2
            )
        else:
            stats['avg_order_value'] = 0.0

        stats['products_bought'] = sorted(list(stats['products_bought']))

    # --- Sort by total_spent descending ---
    customer_stats = dict(
        sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)
    )

    return customer_stats


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    """

    daily = {}

    # --- Aggregate per date ---
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in daily:
            daily[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily[date]['revenue'] += amount
        daily[date]['transaction_count'] += 1
        daily[date]['unique_customers'].add(customer)

    # --- Convert sets to counts ---
    for date, stats in daily.items():
        stats['unique_customers'] = len(stats['unique_customers'])

    # --- Sort chronologically ---
    daily = dict(sorted(daily.items(), key=lambda x: x[0]))

    return daily


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    """

    daily = {}

    # --- Aggregate revenue and transaction count per date ---
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        if date not in daily:
            daily[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily[date]['revenue'] += amount
        daily[date]['transaction_count'] += 1

    # --- Find the date with the highest revenue ---
    if not daily:
        return None  # no data

    peak_date, stats = max(daily.items(), key=lambda x: x[1]['revenue'])

    return peak_date, stats['revenue'], stats['transaction_count']



def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales.
    """

    product_stats = {}

    # --- Aggregate totals per product ---
    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if name not in product_stats:
            product_stats[name] = {
                'total_qty': 0,
                'total_revenue': 0.0
            }

        product_stats[name]['total_qty'] += qty
        product_stats[name]['total_revenue'] += revenue

    # --- Filter products below threshold ---
    low_products = [
        (name, stats['total_qty'], stats['total_revenue'])
        for name, stats in product_stats.items()
        if stats['total_qty'] < threshold
    ]

    # --- Sort by total quantity ascending ---
    low_products.sort(key=lambda x: x[1])

    return low_products
