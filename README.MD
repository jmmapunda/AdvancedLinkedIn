LinkedIn Advanced Automation for Quote Sharing with Pexels and Cloudinary

This project automates the process of sharing motivational quotes with related images on LinkedIn. It fetches random quotes from ZenQuotes API, retrieves related images from Pexels API, uploads them to Cloudinary, overlays the quote text on the image, and then shares the image on LinkedIn using LinkedIn's API.

Features
Fetch Random Quotes: Uses ZenQuotes API to get a random quote of the day.
Search for Images: Uses Pexels API to fetch images related to the quote's theme (e.g., "nature", "sunrise").
Image Overlay: Uses Cloudinary to overlay the quote text on the fetched image, ensuring the text is properly formatted and displayed.
Post on LinkedIn: Uses LinkedIn API to post the image with the quote as a post on LinkedIn.
Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.6+: Make sure Python is installed on your machine. If not, install it from the official Python website.
API Keys:
Pexels API Key: Sign up for an API key from Pexels.
Cloudinary Account: Sign up at Cloudinary and get your API credentials (Cloud name, API Key, and API Secret).
LinkedIn API Access: Set up LinkedIn Developer account and obtain access token and person URN for posting via API. Follow LinkedIn's Developer Documentation.
Installation
Clone the repository to your local machine:


Create a virtual environment and activate it:


Install required dependencies:> check requirements.txt
'pip install -r requirements.txt'


Create a .env file in the project root and add your API keys and credentials:


Usage:
1. Fetch a Random Quote: The program fetches a random quote from the ZenQuotes API. If the author is "unknown," it will replace it with your name (or any placeholder name).

2. Search for Images Based on Keywords: The program randomly selects a keyword from a predefined list (e.g., "nature", "sunset", "ocean") and searches for images related to that keyword on Pexels.

3. Upload Image to Cloudinary: The selected image from Pexels is uploaded to Cloudinary, where the quote is overlaid on the image.

4. Create a LinkedIn Post: The image with the overlayed quote is uploaded to LinkedIn via LinkedIn's API. The post includes the quote text and the author’s name.

5. Automate all the above process without Human interation with the use of GitHub Actions. The code will run everyday at 0500 UTC.

Script Execution
To run the script, simply execute the Python file:


This will perform the following steps:

- Fetch a random quote.
- Search for an image on Pexels based on a related keyword.
- Upload the image to Cloudinary with the quote overlaid on it.
- Post the image to LinkedIn.

Example Workflow
1. Fetch Quote:
The script fetches a random quote from ZenQuotes API. Example response:

json
{
  "q": "The only way to do great work is to love what you do.",
  "a": "Steve Jobs"
}
If the author is "unknown," it defaults to "Me."

2. Search Image from Pexels:
Based on the fetched quote, the script searches for a related image on Pexels. For example, if the quote mentions "great work," it might search for keywords like "inspiration," "motivation," or "success." Example search term:

json
{
  "query": "inspiration",
  "per_page": 10,
  "page": 1
}

3. Upload Image to Cloudinary:
Once the image is selected, the script uploads the image to Cloudinary and overlays the quote text.

4. Post on LinkedIn:
Finally, the script uses the LinkedIn API to post the image with the quote:

If successful, the post will be visible on your LinkedIn profile.

Project Structure

.
├── .env                     # API keys and environment variables
├── linkedin.py    # Main script to fetch quote, search images, upload to Cloudinary, and post on LinkedIn
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

Dependencies
The following Python libraries are required:

requests: For making HTTP requests to APIs.
cloudinary: For uploading and transforming images.
random: For selecting random items (quotes, images).
json: For working with JSON data.

Error Handling
If the quote fetch request fails, the script will print an error message.
If the image search or upload fails, the script will print the error code for debugging.
If the LinkedIn post fails, the script will provide detailed error information to help with debugging.

License
This project is open-source and available under the MIT License.
