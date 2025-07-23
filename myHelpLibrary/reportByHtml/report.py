

import pandas as pd
from ydata_profiling import ProfileReport
import sweetviz as sv

def sweetviz_html_report(df):
    report = sv.analyze(df)
    report.show_html("Sweetviz_report.html")

def create_html_report(df):
    profile = ProfileReport(df , title="Profile Report for the Data",explorative=True , progress_bar=True)
    profile.to_file("Profile data.html")
def find_missing_values(df):
    profile = ProfileReport(df, duplicates={"enabled": True})
    profile.to_file("Duplicates_report.html")

