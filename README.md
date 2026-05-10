# Terms-and-Conditions-Analyzer
AI-Powered Terms & Conditions Risk Analyzer

The project is an NLP-based legal document analysis system designed to help users understand potentially unfavorable clauses in Terms & Conditions, contracts, and policy documents. The system accepts PDF files, images, or plain text as input and automatically extracts and analyzes the content using Natural Language Processing and semantic similarity techniques.
The application segments the document into individual clauses and evaluates each clause independently to identify risks such as hidden charges, automatic renewals, liability waivers, data-sharing permissions, arbitration clauses, and unfair termination rights.
The analysis pipeline combines:
•	OCR/text extraction 
•	NLP preprocessing 
•	clause segmentation 
•	semantic embedding similarity 
•	heuristic risk scoring 
•	optional LLM enhancement 
Each clause receives:
•	a risk category 
•	risk score 
•	contextual explanation 
•	highlighted problematic phrases 
The system focuses on explainable AI rather than simple keyword detection, making the analysis context-aware and more reliable for real-world legal text understanding.
The project is lightweight, privacy-friendly, and designed to work without storing user data.
