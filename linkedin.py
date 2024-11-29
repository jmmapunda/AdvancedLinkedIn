import os
from datetime import datetime

import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import requests
import random
import json
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv

load_dotenv() #This line is commented to allow GitHub actions to work smooth, but on local machine you need it.
cloudname = os.getenv('cloudname')
APIKEY = os.getenv('APIKEY')
APISECRET = os.getenv('APISECRET')
PEXELKEY = os.getenv('PEXELKEY')
access_token = os.getenv('access_token')
person_urn = os.getenv('person_urn')
x_access_token = os.getenv('x_access_token')
x_access_token_secret = os.getenv('x_access_token_secret')
screen_name = "johncaptain007"
x_consumer_key = os.getenv('x_consumer_key')
x_consumer_secret = os.getenv('x_consumer_secret')

# URL for ZenQuotes API
url = "https://zenquotes.io/api/random"

# Make a GET request to fetch the random quote of the day
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    quote = data[0]['q']  # Quote text
    author = data[0]['a']  # Author's name
    if author == 'unknown':
        author = 'Me'
quote = f'"{quote}"'  # Add quotes around the quote
author = f'"{author}"'
# Print the quote and author
print(f"Quote: {quote}\nAuthor: {author}")

#list of keywords to choice from, and search for images
imagekeywords = [
    "Nature", "Ocean", "Sunrise", "Forest", "Sky", "Clouds", "Wildlife", "Desert",
    "Waterfall", "Lake", "Grasslands", "Autumn", "Snow", "Canyon", "Meadows", "Fog",
    "Waves", "Thunderstorm", "Aurora", "Garden", "Pathway", "Cliffs", "Rocks", "Leaves",
    "Reflection", "Horizon", "Peaceful", "Tranquility", "Flowers", "Spring", "Sunbeam",
    "Mountains", "River", "Sunset", "Trees", "Hills", "Valley", "Beach", "Sand",
    "Winter", "Summer", "Rain", "Bloom", "Lightning", "Dew", "Vine", "Fields", "Wilderness"]
search_image = random.choice(imagekeywords)
# Endpoint for searching photos
url = "https://api.pexels.com/v1/search"

# Define parameters
params = {
    "query": search_image,  # The search term (can be anything)
    "per_page": 50,  # Number of results per page (maximum is 80)
    "page": 1  # The page number (for pagination)
    }

# Headers with the API key for authentication
headers = {
    "Authorization": PEXELKEY
    }

# Send GET request to Pexels API
response = requests.get(url, headers=headers, params=params)
image_list = []
# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # print(data)
    for photo in data["photos"]:
        image_list.append(photo["src"]["original"])
else:
    print(f"Error: {response.status_code}")
#from image_list choice one image to work with
image_to_edit = random.choice(image_list)
print(image_to_edit)

# Configuration
cloudinary.config(
    cloud_name=cloudname,
    api_key=APIKEY,
    api_secret=APISECRET,
    secure=True
    )

# Upload an image
upload_result = cloudinary.uploader.upload(image_to_edit, public_id="quotes")
print("Uploaded Image URL:", upload_result["secure_url"])

# Set the maximum number of words per line
max_words_per_line = 6  # Example: 6 words per line (adjust based on your layout)

# Split the quote into a list of words
words = quote.split()

# Group the words into lines based on the maximum number of words per line
quote_lines = []
for i in range(0, len(words), max_words_per_line):
    quote_lines.append(" ".join(words[i:i + max_words_per_line]))

# Join the lines with %0A for line breaks
quote_today = "%0A".join(quote_lines)

# Add text overlay to the image
text_overlay_url, _ = cloudinary_url(
    "quotes",  # Use the correct public ID for the uploaded image
    transformation=[
        {"width": 800, "height": 1000, "crop": "fill", "gravity": "center"},  # Resize to 1200x650
        {
            # "color": "black",  # Use a named overlay for simplicity
            "opacity": 80,  # Adjust opacity (0 to 100)
            "width": 600,
            "height": 800,
            "crop": "fill",
            "gravity": "center"
            },
        {
            "overlay": {
                "font_family": "Helvetica",
                "font_size": 30,
                "text": f"{quote_today}%0A%0A{author}",  # URL-encoded spaces and line break
                "max_width": 600,
                'text_align': "center"
                # "line_breaks": True,
                },
            "color": "black",
            "gravity": "center",  # Center the text
            "x": 10,  # Horizontal padding
            "y": 10,  # Vertical padding
            "crop": "fit"  # Fit the text within the image width
            }
        ]
    )
print("Image with Text Overlay URL:", text_overlay_url)

##############LinkedIn Part

# Step 1: Image create upload link
url = "https://api.linkedin.com/v2/assets?action=registerUpload"
headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json"
    }

image_url = text_overlay_url  # Replace with your image URL

payload = {
    "registerUploadRequest": {
        "owner": person_urn,  # Replace with your LinkedIn person URN
        "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    # Image registered successfully
    upload_info = response.json()
    asset = upload_info['value']['asset']
    linkedin_upload_url = upload_info['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    print(f"Image uploaded. Asset: {asset}")
else:
    print(f"Failed to upload image: {response.status_code}")
    print(response.text)
    exit()

# Step 2: Download the image from the URL and upload it to LinkedIn
image_response = requests.get(image_url)

if image_response.status_code == 200:
    headers = {"Content-Type": "image/jpeg"}  # Adjust if a different image type
    response = requests.put(linkedin_upload_url, headers=headers, data=image_response.content)

    # Check the response status
    if response.status_code == 201:
        print("Image uploaded successfully!")
    else:
        print(f"Failed to upload image: {response.status_code}")
        print(response.text)
else:
    print("Failed to download image from the URL.")

# Step 3: Create the post
post_quote = f"{quote},\n{author}"
# Create the post JSON with media
post_json = {
    "author": person_urn,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": post_quote  # The text of the post
                },
            "shareMediaCategory": "IMAGE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Center statge!"
                        },
                    "media": asset,  # The asset URN you received
                    "title": {
                        "text": "Sample Image"
                        }
                    }
                ]
            }
        },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
    }

response = requests.post(url, json=post_json, headers=headers)

# Check the response status
if response.status_code == 201:
    print("Post created successfully!")
else:
    print(f"Failed to create post: {response.status_code}")
    print(response.json())  # Print the full response for debugging

########### X post
# Make the request using saved tokens
oauth = OAuth1Session(
    x_consumer_key,
    client_secret=x_consumer_secret,
    resource_owner_key=x_access_token,
    resource_owner_secret=x_access_token_secret,
)

#  Upload media to X
media_upload_url = "https://upload.twitter.com/1.1/media/upload.json"
files = {"media": image_response.content}
response = oauth.post(media_upload_url, files=files)
print(response)
media_id = response.json()["media_id"]
print("Uploaded media with ID:", media_id)

# Payload for the tweet
if datetime.now().weekday() == 1 or 4: # on tuesday and friday will post tweet with image.
    payload = {
        "text": post_quote,
        "media": {
            "media_ids": [str(media_id)]
            }
        }
else:
    payload = {
        "text": post_quote,
        }

# Sending the tweet
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Print the response
json_response = response.json()
print(json.dumps(json_response['data']['id'], indent=4, sort_keys=True))

