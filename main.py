def main():
    """
    Main execution function for the Sales Analytics System.
    """

    print("========================================")
    print("        SALES ANALYTICS SYSTEM")
    print("========================================\n")

    try:
        # ----------------------------------------------------
        # READ SALES DATA
        # ----------------------------------------------------
        print("[1/10] Reading sales data...")
        raw_data = load_sales_data("sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} transactions\n")

        # ----------------------------------------------------
        # [2/10] PARSE & CLEAN
        # ----------------------------------------------------
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records\n")

        # ----------------------------------------------------
        # [3/10] FILTER OPTIONS
        # ----------------------------------------------------
        print("[3/10] Filter Options Available:")

        regions = sorted({t["Region"] for t in transactions})
        print("Regions:", ", ".join(regions))

        amounts = [t["UnitPrice"] * t["Quantity"] for t in transactions]
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()
        print()

        if choice == "y":
            region = input("Enter region to filter (or press Enter to skip): ").strip()
            min_amt = input("Minimum amount (or press Enter): ").strip()
            max_amt = input("Maximum amount (or press Enter): ").strip()

            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None

            transactions = filter_transactions(
                transactions,
                region=region if region else None,
                min_amount=min_amt,
                max_amount=max_amt
            )

            print(f"✓ Filter applied. Remaining records: {len(transactions)}\n")

        # ----------------------------------------------------
        # [4/10] VALIDATION
        # ----------------------------------------------------
        print("[4/10] Validating transactions...")
        valid, invalid = validate_transactions(transactions)
        print(f"✓ Valid: {len(valid)} | Invalid: {len(invalid)}\n")

        # Use only valid transactions for analysis
        transactions = valid

        # ----------------------------------------------------
        # [5/10] ANALYSIS
        # ----------------------------------------------------
        print("[5/10] Analyzing sales data...")
        _ = calculate_total_revenue(transactions)
        _ = region_wise_sales(transactions)
        _ = top_selling_products(transactions)
        _ = customer_analysis(transactions)
        _ = daily_sales_trend(transactions)
        _ = find_peak_sales_day(transactions)
        _ = low_performing_products(transactions)
        print("✓ Analysis complete\n")

        # ----------------------------------------------------
        # [6/10] FETCH API PRODUCTS
        # ----------------------------------------------------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # ----------------------------------------------------
        # [7/10] ENRICH SALES DATA
        # ----------------------------------------------------
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        success_rate = (enriched_count / len(enriched_transactions)) * 100
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)\n")

        # ----------------------------------------------------
        # [8/10] SAVE ENRICHED DATA
        # ----------------------------------------------------
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # ----------------------------------------------------
        # [9/10] GENERATE REPORT
        # ----------------------------------------------------
        print("[9/10] Generating report...")
        generate_sales_report(transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt\n")

        # ----------------------------------------------------
        # [10/10] COMPLETE
        # ----------------------------------------------------
        print("[10/10] Process Complete!")
        print("========================================")

    except Exception as e:
        print("An unexpected error occurred:")
        print(str(e))
        print("Please check your input files and try again.\n")
