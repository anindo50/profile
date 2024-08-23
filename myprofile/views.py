from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import pdf_to_text
import os
from pdfminer.high_level import extract_text
from PIL import Image
import pytesseract
from .utils import pdf_to_word 
from django.conf import settings
import shutil


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

def file_upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('pdf_file')
        if uploaded_file:
            # Save the uploaded PDF file temporarily
            fs = FileSystemStorage()
            pdf_path = fs.save(uploaded_file.name, uploaded_file)
            pdf_full_path = fs.path(pdf_path)
            
            # Define the path for the output text file
            txt_file_name = os.path.splitext(uploaded_file.name)[0] + '.txt'
            txt_full_path = os.path.join(fs.location, txt_file_name)
            print("txt_file_name",txt_file_name ," ", "txt_full_path",txt_full_path)

            try:
                # Convert PDF to text
                text_file = pdf_to_text(pdf_full_path, txt_full_path)
                
                # Provide the URL to download the text file
                txt_file_url = fs.url(os.path.basename(text_file))
                print("file created")
                return render(request, 'file.html', {'txt_file_url': txt_file_url})
            except Exception as e:
                return HttpResponse(f"An error occurred while processing the PDF: {e}")
        else:
            return HttpResponse("No file uploaded")
    return render(request, 'file.html')


def convert_pdf_to_word_view(request):
    media_root = settings.MEDIA_ROOT
    for filename in os.listdir(media_root):
        file_path = os.path.join(media_root, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)  # Remove file or symlink
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path) 


    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        pdf_filename = fs.save(pdf_file.name, pdf_file)
        pdf_file_url = fs.url(pdf_filename)
        
        # Convert PDF to Word
        output_filename = os.path.splitext(pdf_file.name)[0] + '.docx'
        output_path = fs.path(output_filename)
        
        pdf_to_word(fs.path(pdf_filename), output_path,dpi=300,lang='eng')
        
        # Provide a link to download the Word file
        word_file_url = fs.url(output_filename)
        
        return render(request, 'convert_pdf_to_word.html', {
            'pdf_file_url': pdf_file_url,
            'word_file_url': word_file_url
        })
   
    
    return render(request, 'convert_pdf_to_word.html')



