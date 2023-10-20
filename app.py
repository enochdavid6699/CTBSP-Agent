#Imort statements
from black import nullcontext
import requests
import os
from dotenv import load_dotenv
import openai


#Import For stable Diffusion
import requests
import json


# Load environment variables from the .env file
load_dotenv()

#OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")



# TOPIC GENERATION FUNCTION
def generate_topic(category):
    prompt = f"Generate a topic related to the category: {category}"
        
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,  # You can adjust the max_tokens as needed
        n=3,            # You can adjust n as needed to get multiple suggestions
        stop=None
    )
        
    topics = [choice.text.strip() for choice in response.choices]
        
    return topics

# BLOG GENERATION FUNCTION
def generate_blog_content(topic):
    prompt = f"Write a blog post on the following topic: {topic}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,  # You can adjust the max_tokens as needed for the length of the blog
    )
    
    blog_content = response.choices[0].text.strip()
    
    return blog_content

# SEO KEYWORD GENERATION FUNCTION
def generate_seo_keywords(topic):
    prompt = f"Generate seo keywords for the following topic: {topic}"
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,  # You can adjust the max_tokens as needed
            n=3,            # You can adjust n as needed to get multiple suggestions
            stop=None
        )
    return response.choices[0].text


# IMAGE PROMPT GENERATION FUNCTION
# def generate_image_prompts(topic, num_prompts=3):
#     prompts = []
#     prompt = f"I am making a blog on the topic: {topic}. Give me a prompt for image generation for this topic."
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=200,  # You can adjust the max_tokens as needed
#         n=num_prompts,   # Number of prompts you want to generate
#         stop=None
#     )
    
#     for choice in response.choices:
#         prompts.append(choice.text.strip())
    
#     return prompts


# IMAGE PROMPT GENERATION FUNCTION
def generate_image_prompt(topic):
    prompt = f"I am making a blog on the topic: {topic}. Give me a prompt for image generation for this topic."
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,  # You can adjust the max_tokens as needed
            n=3,            # You can adjust n as needed to get multiple suggestions
            stop=None
        )
    return response.choices[0].text

# IMAGE GENERATION
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url




# def generate_image(prompt):
#     url = "https://stablediffusionapi.com/api/v3/text2img"

#     payload = {
#         "key": "",
#         "prompt": prompt,
#         "negative_prompt": None,
#         "width": "512",
#         "height": "512",
#         "samples": "1",
#         "num_inference_steps": "20",
#         "seed": None,
#         "guidance_scale": 7.5,
#         "safety_checker": "yes",
#         "multi_lingual": "no",
#         "panorama": "no",
#         "self_attention": "no",
#         "upscale": "no",
#         # "embeddings_model": null,
#         "webhook": None,
#         "track_id": None
#     }

#     headers = {
#         'Content-Type': 'application/json'
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     return response.text





# INPUT FOR CATEGORY
category = input("Please enter a category: ")

# MANUAL APPROVAL OF TOPICS 
approved_topics = []
if category:
    while True: 
        topics = generate_topic(category)
        for i, topic in enumerate(topics, start=1):
            print(f"Generated Topic {i}:\n{topic}\n")
        approval = input("Do you approve any of these topics? Enter the number(s) of the topic(s) you approve (e.g., '1 3'), or 'n' to generate a new topic: or 'y' if you want to approve all topics: ").strip().lower()
        if approval == 'n':
            print("Generating a new topic...\n")
        elif approval == 'y':
            approved_topics = topics
            break
        else:
            approved_topics = [topics[int(index) - 1] for index in approval.split()]
            break

print(f"Approved Topic: {approved_topics}")

# APPROVAL FUNCTIONS (INNER)
def approve_blog(blog_content , topic):
    print("--- Blog Topic ---")
    print(topic)
    print("\n")
    print("--- Blog Content ---")
    print(blog_content)
    print("\n")
    approval = input("Do you approve this blog? (y/n): ").strip().lower()
    
    if approval == 'y': 
        return 'y'
    else:
        return 
        
# APPROVAL FUNCTIONS (OUTER)  
if approved_topics:
    approved_blogs = {}
    for topic in approved_topics:
        blog_seo = generate_seo_keywords(topic)
        # blog_image_prompts = generate_image_prompts(topic, num_prompts=3) 
        blog_image_prompt = generate_image_prompt(topic)
        image_url = generate_image(blog_image_prompt) 
        while True:
            blog_content = generate_blog_content(topic)
            if approve_blog(blog_content, topic):
                approved_blogs[topic] = {
                    'content': blog_content,
                    'seo_keywords': blog_seo,
                    'image_prompt': blog_image_prompt,
                    'image_url': image_url
                }
                break


    # Print or save the approved blogs
    for topic, data in approved_blogs.items():
        print(f"--- Approved Blog for {topic} ---")
        print("Content:")
        print(data['content'])
        print("\n")
        print("SEO Keywords: ")
        print(data['seo_keywords'])
        print("\n")
        print("Image Prompts: ")
        
        # for i, prompt in enumerate(data['image_prompt'], start=1):
        #     print(f"Image Prompt {i}:")
        #     print(prompt)
        
        print(data['image_prompt'])
        print("\n")
        print(data['image_url'])
        print("\n")