README: AgriSearch Data Processing Pipeline
This directory contains the Python scripts responsible for the ETL (Extract, Transform, Load) pipeline that powers the AgriSearch engine. The goal of this pipeline is to take raw, unstructured data scraped from multiple university websites and transform it into a clean, unified, and chunked format ready for ingestion into a vector database.
The Data Challenge
The core challenge is that each university extension website has a completely different structure, data format, and level of quality. This pipeline is designed to handle that diversity by:
Normalizing data from different scrapers into a single, consistent schema.
Cleaning and standardizing fields like dates and URLs.
Chunking large documents into smaller, semantically relevant pieces for effective use in a RAG (Retrieval-Augmented Generation) system.
Generating consistent metadata and snippets for each document.
The Pipeline Workflow
The process is executed through a series of scripts, each with a specific job.
1. converge_label.py - The Normalizer
Purpose: This script acts as a "schema enforcer." It takes the unique JSON output from an individual web scraper (e.g., revised_missu_whoop_pdf.json) and transforms it into a standardized format.
Process:
It maps inconsistent field names (published_date, home_url) to a master schema (pub_date, main_url).
It adds consistent metadata, like the school name.
The output is a standardized file (e.g., missouri_use_me.json) where every document has the same set of keys. This is repeated for each of the nine data sources.
2. merge_all_data.py - The Unifier
Purpose: To combine all the individual, standardized JSON files into a single master dataset.
Process:
It iterates through a list of the *_use_me.json files.
It intelligently loads and extends a master list, creating a single, large JSON array.
The output, merged_extension_data.json, is the complete, raw dataset for the entire project.
3. prepare_data.py - The AI Prepper & Chunker
Purpose: This is the most critical script for preparing the data for the semantic search engine. It takes the large, merged dataset and makes it AI-ready.
Process:
Loads the merged_extension_data.json file.
Generates Snippets: For each document, it creates a consistent 500-word summary snippet that will be displayed in the search results.
Chunks Documents: Using the RecursiveCharacterTextSplitter from LangChain, it breaks down the full text of each PDF into smaller, overlapping chunks (800 characters with 100 characters of overlap). This is essential for the accuracy of the RAG system.
Attaches Metadata: It ensures that every single chunk retains all the essential metadata from the parent document (headline, URL, school, pub_date, etc.).
The output, *_chunked.json, is the final, AI-ready dataset that will be used to build the vector database.
4. check.py - The Quality Assurance Tool
Purpose: A simple but vital utility script to verify the integrity of the final ChromaDB vector database.
Process:
It connects to the persistent chroma_db on disk.
It fetches a few sample items and prints their metadata.
This allows the developer to quickly check that the database was built correctly and that all necessary metadata fields (like summary) were successfully indexed.
How to Run the Pipeline
To regenerate the entire dataset from the raw scraper outputs:
Run converge_label.py for each raw JSON file to create the standardized *_use_me.json files.
Run merge_all_data.py to combine the standardized files into merged_extension_data.json.
Run prepare_data.py to chunk the merged file and create the final *_chunked.json.
(After indexing into ChromaDB) Run check.py to validate the vector database.
This disciplined, multi-step process is what enables the AgriSearch engine to provide clean, reliable, and relevant results from a diverse and messy collection of source data.
