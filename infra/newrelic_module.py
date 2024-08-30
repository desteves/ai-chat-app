"""_summary_
"""
import json
import pulumi_newrelic as newrelic

def declare_new_relic_resources():
    """_summary_
    """
    # Load the JSON configuration
    dash = ""
    with open('../dashboard.json', encoding="utf-8") as f:
        dash_obj = json.load(f)
        dash = json.dumps(dash_obj)

    # Create the New Relic dashboard
    newrelic.OneDashboardJson(
        resource_name='my_cool_dashboard',
        json=dash,
    )
