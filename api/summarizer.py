import os

from transformers import pipeline
from nltk.stem.porter import PorterStemmer

from PyPDF2 import PdfReader 

import re

class Summarizer:
    def __init__(self):
        self.load_models() # Load models
    def load_models(self):
        # Load model directly
        # Use a pipeline as a high-level helper
        self.summarizer = pipeline("summarization", model="sinking8/text_summarizer_finetuned")
    def preprocess(self,texts):
        # Processed
        proc_texts = []
        
        for text in texts:
            text1 = " ".join([re.sub('\W+','',word) for word in text.split()])
            proc_texts.append(text1)

        # Return proc_texts nested lists
        return proc_texts
            
    def generate_summary(self,texts):
        # Process Text
        preprocessed_texts = self.preprocess(texts)

        # Combine multiple segments
        compiled_text = "\n".join(preprocessed_texts)

        # Return Texts
        return self.summarizer(compiled_text, max_length=20000, min_length=30, do_sample=False)[0]['summary_text']
    
    def generate_pdf_to_text(self,pdf_file):
  
        # creating a pdf reader object 
        reader = PdfReader(os.path.join("./cache",pdf_file)) 

        # getting a specific page from the pdf file
        texts = []
        for page in reader.pages:
            texts.append(page.extract_text()) 

        # Return Summary
        summary = self.generate_summary(texts)

        return summary
    
    def generate_img_to_text(self,img_file):
        # Sample
        return ""
        