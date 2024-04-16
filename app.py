import pandas as pd
from io import StringIO
import streamlit as st
from controller import CTLJira as ctl

from st_pages import Page, show_pages, add_page_title

def main():
    show_pages(
            [
                Page("pages/jira.py", "Jira", ":newspaper:")
            ]
        )
        
        
if __name__ == "__main__":
    main()

            

    
