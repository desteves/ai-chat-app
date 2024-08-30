"""_summary_
"""
import json
import pulumi_newrelic as newrelic

def declare_new_relic_resources():
    """_summary_
    """
    # Load the JSON configuration
    dash = ""
    with open('../simpledashboard.json', encoding="utf-8") as f:
        dash = json.load(f)
        # print(dash)

    # Create the New Relic dashboard
    newrelic.OneDashboardJson(
        'my_dashboard',
        # json=dash,
    )
