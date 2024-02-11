from api.report import *
from api.llm import *

import os

summaries = ["Hello All the best","ABC is 20 year old","He is a male and a swimmer","Had Diabetes for around 35 years"]

report  = Report()
llm =  LLM()

titles = llm.generate_titles(summaries)
print(titles)
report.generate_report(summaries,titles=titles)