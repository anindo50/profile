from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
# from .utils import pdf_to_text
import os
# from pdfminer.high_level import extract_text
# from PIL import Image
# import pytesseract
from .utils import text_gen
# from .utils import pdf_to_word
from django.conf import settings
# import shutil
import yt_dlp
from .forms import YouTubeDownloadForm
from .voice import customize_tts
# import pyautogui
import time
from django.http import JsonResponse
from .models import NewsArticle
from datetime import datetime
import requests
import re

def my_view(request):
    return render(request, 'cv.html')

def cv_view(request):
    return HttpResponse("Hello, world!")

# def file(request):
#     if request.method == "POST":
#         uploaded_file = request.FILES.get('pdf_file')  # Use FILES to get the file
#         if uploaded_file:

#             try:
#                 text = extract_text(uploaded_file)
    
#     # Save the extracted text to a text file with UTF-8 encoding
#                 with open(settings.MEDIA_ROOT, 'w', encoding='utf-8') as txt_file:
#                     txt_file = txt_file.write(text)
#                 # pdf_to_text(uploaded_file,settings.MEDIA_ROOT)
#                 # # Read the file content, ignoring errors
#                 # file_content = uploaded_file.read().decode('utf-8', errors='ignore')
#                 # print(file_content)  # Print file content to console or log
#                 return render(request, 'file.html', {'txt_file_url': txt_file})
#             except Exception as e:
#                 return HttpResponse(f"An error occurred while reading the file: {e}")
#         else:
#             return HttpResponse("No file uploaded")
#     return render(request, 'file.html')




######### pdf to txt ##################

# def file_upload(request):
#     if request.method == "POST":
#         uploaded_file = request.FILES.get('pdf_file')
#         if uploaded_file:
#             # Save the uploaded PDF file temporarily
#             fs = FileSystemStorage()
#             pdf_path = fs.save(uploaded_file.name, uploaded_file)
#             pdf_full_path = fs.path(pdf_path)
            
#             # Define the path for the output text file
#             txt_file_name = os.path.splitext(uploaded_file.name)[0] + '.txt'
#             txt_full_path = os.path.join(fs.location, txt_file_name)
#             print("txt_file_name",txt_file_name ," ", "txt_full_path",txt_full_path)

#             try:
#                 # Convert PDF to text
#                 text_file = pdf_to_text(pdf_full_path, txt_full_path)
                
#                 # Provide the URL to download the text file
#                 txt_file_url = fs.url(os.path.basename(text_file))
#                 print("file created")
#                 return render(request, 'file.html', {'txt_file_url': txt_file_url})
#             except Exception as e:
#                 return HttpResponse(f"An error occurred while processing the PDF: {e}")
#         else:
#             return HttpResponse("No file uploaded")
#     return render(request, 'file.html')

###########################################################################################################


################ pdf to word with ocr ####################


# def convert_pdf_to_word_view(request):
#             # clear media file
#     # media_root = settings.MEDIA_ROOT
#     # for filename in os.listdir(media_root):
#     #     file_path = os.path.join(media_root, filename)
#     #     if os.path.isfile(file_path) or os.path.islink(file_path):
#     #         os.remove(file_path)  # Remove file or symlink
#     #     elif os.path.isdir(file_path):
#     #         shutil.rmtree(file_path) 


#     if request.method == 'POST' and request.FILES['pdf_file']:
#         pdf_file = request.FILES['pdf_file']
#         fs = FileSystemStorage()
#         pdf_filename = fs.save(pdf_file.name, pdf_file)
#         pdf_file_url = fs.url(pdf_filename)
        
#         # Convert PDF to Word
#         output_filename = os.path.splitext(pdf_file.name)[0] + '.docx'
#         output_path = fs.path(output_filename)
        
#         pdf_to_word(fs.path(pdf_filename), output_path,dpi=300,lang='eng')
        
#         # Provide a link to download the Word file
#         word_file_url = fs.url(output_filename)
        
#         return render(request, 'convert_pdf_to_word.html', {
#             'pdf_file_url': pdf_file_url,
#             'word_file_url': word_file_url
#         })
   
    
#     return render(request, 'convert_pdf_to_word.html')

#########################################################################################

def download_video(request):
    file_url = None
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['url']
            download_path = os.path.join(settings.MEDIA_ROOT, 'downloads')  # Define the path where videos will be saved

            # Ensure the download directory exists
            if not os.path.exists(download_path):
                os.makedirs(download_path)

            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save to downloads directory
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    # Generate the file path for the downloaded video
                    file_name = f'{info_dict["title"].replace(" ", "")}.{info_dict["ext"]}'
                    file_name = file_name.replace("|","")
                    file_url = os.path.join(settings.MEDIA_URL, 'downloads', file_name)
                    file_url = file_url.replace("\\","/")
                    
                    print(file_url)
                    
            except Exception as e:
                return HttpResponse(f"Error during download: {e}")
    else:
        form = YouTubeDownloadForm()

    return render(request, 'download.html', {'form': form, 'file_url': file_url})


def voice(request):
    output = ""
    url = ""
    if "submit" in request.POST:
        text = request.POST.get('voice')
        if text:
            print(text.split(' ')[0])
            output = text.split(' ')[0] + ".wav"
            output_path = os.path.join(settings.MEDIA_ROOT, output) 
            
            voi = customize_tts(text,output_path)
            
            url = output_path.replace("\\","/")
            fs = FileSystemStorage()
            path = os.path.join(output)
            url = fs.url(path)
            return render(request,'voice.html',{'voice':url})
        

    
    return render(request,'voice.html')


def text_genaration(request):
    gen_tex = None
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            gen_tex = text_gen(text)
            if gen_tex:
                print(gen_tex)
    return render(request, "text.html", {"gen": gen_tex})


# screenshot_dir = os.path.join(settings.MEDIA_ROOT, "screenshots")
# os.makedirs(screenshot_dir, exist_ok=True)  # Ensure the folder exists

# def take_screenshot(request):
#     """Capture and save a screenshot, then return its URL."""
#     timestamp = time.strftime("%Y%m%d-%H%M%S")
#     screenshot_name = f"screenshot_{timestamp}.png"
#     screenshot_path = os.path.join(screenshot_dir, screenshot_name)
#     screenshot_url = f"{settings.MEDIA_URL}screenshots/{screenshot_name}"

#     # Take the screenshot
#     screenshot = pyautogui.screenshot()
#     screenshot.save(screenshot_path)

#     # return JsonResponse({"message": "Screenshot saved", "screenshot_url": screenshot_url})
#     return render(request,"take_ss.html",{"message": "Screenshot saved","screenshot_url": screenshot_url})


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options for headless browsing and User-Agent header
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run the browser in headless mode
    chrome_options.add_argument('--no-sandbox')  # Required for running in certain environments (e.g., Docker)
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage
    chrome_options.add_argument('start-maximized')  # Start browser in maximized mode
    chrome_options.add_argument('disable-infobars')  # Disable the infobar
    chrome_options.add_argument('--disable-extensions')  # Disable extensions
    chrome_options.add_argument('--disable-gpu')  # Disable GPU (needed for headless mode)

    # Set the custom User-Agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Create the WebDriver with the above options
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Fetch the latest news articles by scraping
def fetch_news():
    url = 'https://www.dhakatribune.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    driver = create_driver()
    # response = requests.get(url, headers=headers)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    headlines = soup.find_all('a', class_='link_overlay')
    news_dic = {}  # Initialize the dictionary to store article details
    
    driver = create_driver()  # Open the browser only once

    for h in headlines[:5]:
        article_url = h.get('href').strip()
        article_title = h.get('title')
        if article_url.startswith("//"):
            article_url = article_url.replace("//","https://")

            if not article_url or not article_title:  # Skip if URL or title is missing
                continue

            print(f"Fetching article: {article_title} ({article_url})")

            driver.get(article_url)  # Open article page
            time.sleep(3)  # Allow the page to load

            article_soup = BeautifulSoup(driver.page_source, 'html.parser')
            container = article_soup.find("div", class_="content_detail_content_inner")

            if not container:  # If no content is found, skip this article
                print(f"Warning: No content found for {article_title}")
                continue

            news_list = []
            all_p = container.find_all("p")

            for p in all_p:
                text = p.text.replace("', '"," ").strip()
                if text:
                    news_list.append(text)
                    print(text)
            
            news_dic[article_title] = news_list  # Store article text

    driver.quit()  # Close the browser after all articles are processed
    return news_dic


# def news_view(request):
    
#     today = datetime.today().date()
#     # if not NewsArticle.objects.exists():
#     #     news_data = fetch_news()  # Fetch the news dictionary
#     #     for title, paragraphs in news_data.items():
#     #         # Clean the paragraphs by removing unwanted spaces and line breaks
#     #         content = "\n".join([p.strip() for p in paragraphs])  # Strip unnecessary spaces
#     #         content = content.replace("\n", " ")  # Replace line breaks with spaces
            
#     #         # Save the cleaned content to the database
#     #         NewsArticle.objects.create(title=title, content=content, date = today)
    
    
#     print(today)
#     all_data = NewsArticle.objects.all()
#     print(all_data)
#     new_dic = dict()
#     for data in all_data:
        
#         date = data.date
#         title = data.title
#         content = data.content
        
#         print("i am today",today)
#         print("i am date",date)
        
        
        
#         new_dic[title] = content
#         return render(request, 'news.html', {'news_data': new_dic})
        
#         if date != today:
#             print("i am in differ")
#             news_data = fetch_news()
#             if date is not None:
#                 for title, paragraphs in news_data.items():
#                     model = NewsArticle(title = title, content = paragraphs, date = today)
#                     model.save()
#                 return render(request, 'news.html', {'news_data': news_data})


def news_view(request):
   
    today = datetime.today().date()
    
    print("Today's date:", today)

    # Fetch all news articles
    all_data = NewsArticle.objects.all()
    print("Fetched articles:", all_data)

    new_dic = {}

    for data in all_data:
        date = data.date
        title = data.title
        content = data.content

        print("Processing article:", title)
        print("Article date:", date)
        content = content.replace("[","").replace("]","").replace("', '","").replace('", "',' ')
        content = re.sub(r"',\s*\"|\",\s*'", " ", content)

        new_dic[title] = content  # Store each article's title and content
    
    # Move render outside the loop
    return render(request, 'news.html', {'news_data': new_dic})


def update_news(request):
    today = datetime.today().date()
    new_dic = {}
    news_data = fetch_news()
    NewsArticle.objects.all().delete()
    for t , content in news_data.items():
        # content = content.replace("[","").replace("]","").replace("', '","")
        # content = re.sub(r"',\s*\"|\",\s*'", " ", content)
        new_dic[t] = content
    
    for title , paragraph in new_dic.items():
        model = NewsArticle(title = title, content = paragraph, date = today)
        model.save()
    
    return redirect("news_page")
    # return render(request, 'news.html', {'news_data': new_dic})





def get_most_profitable_stocks():
    base_url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?formatted=true&lang=en-US&region=US&scrIds=most_actives&corsDomain=finance.yahoo.com"
    
    # Specify a user-agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(base_url, headers=headers)
    data = response.json()
    
    stocks_info = []

    if 'finance' in data and 'result' in data['finance'] and data['finance']['result']:
        quotes = data['finance']['result'][0]['quotes']
        for quote in quotes:
            symbol = quote['symbol']
            name = quote['shortName']
            price = quote['regularMarketPrice']['raw']
            change_percent = quote['regularMarketChangePercent']['raw']

            # Fetch previous day's closing price
            previous_close = quote['regularMarketPreviousClose']['raw']

            # Calculate increase or decrease rate in percentage
            if previous_close > 0:
                increase_rate = ((price - previous_close) / previous_close) * 100
            else:
                increase_rate = 0
                
            decrease_rate = change_percent - increase_rate

            stocks_info.append({'symbol': symbol, 'name': name, 'price': price, 'change_percent': change_percent,
                                'increase_rate': f"{increase_rate:.7f}", 'decrease_rate': f"{decrease_rate:.7f}",})
    
    return stocks_info




def stock_market_view(request):
    stocks = get_most_profitable_stocks()
    return render(request, 'stocks.html', {'stocks': stocks})