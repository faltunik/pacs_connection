# pacs_connection

Implement PACS Communication via pynetdicom library

DEMO (For PACS Config and Browse): https://youtu.be/RiHZFhPxyy0

SETUP:
Please Install : pynetdicom and pydicom library

Running The App:
Currently Only pacs_config and browse feature is available.
You can test both by running search_download.py file.

Current Feature Includes:
1. Adding New PACS Server: We have checker to check valid and unique pair of ip_address, port nu and unique AET
2. Verify, Delete and Update PACS Server Details
3. Browse Files using Patient Name, Id or Accession number.
4. Filters for Date Range, Accession number, Patient Name/Id



Upcoming Features:
1. Download DICOM files
2. Search Files across various PACS Server, currently you can only select one pacs server
3. Upload DICOM Files


Upcoming Enhancement:
1. Adding Test Cases
2. Providing More information on search
