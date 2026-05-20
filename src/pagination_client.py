def export_reports(next_token):
    reports = []

    while next_token:
        response = fetch_page(next_token)

        reports.extend(response["records"])

    return reports
