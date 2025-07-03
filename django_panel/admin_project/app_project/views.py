# import os
# import json
# from django.http import HttpResponse
# from django.conf import settings

# def list_all_folders_view(request):
#     base_path = r"E:\product_images"
#     base_url = settings.MEDIA_URL.rstrip('/')

#     if not os.path.exists(base_path):
#         return HttpResponse("❌ Base path does not exist.")

#     entries = []

#     # Walk and collect all files and folders
#     for root, dirs, files in os.walk(base_path):
#         for file in files:
#             rel_path = os.path.relpath(os.path.join(root, file), base_path).replace("\\", "/")
#             full_path = os.path.join(base_path, rel_path.replace("/", os.sep))
#             file_info = {
#                 "name": file,
#                 "rel_path": rel_path,
#                 "full_path": full_path,
#                 "folder": os.path.dirname(rel_path).replace("/", " > ") or "Root"
#             }

#             if file.lower().endswith(".json"):
#                 try:
#                     with open(full_path, 'r', encoding='utf-8') as f:
#                         file_info["json_data"] = json.load(f)
#                 except Exception as e:
#                     file_info["json_data"] = f"❌ Error reading JSON: {e}"

#             if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
#                 file_info["is_image"] = True

#             entries.append(file_info)

#     # Generate HTML
#     html = """
#     <html>
#     <head>
#         <title>📂 Product Image Listing</title>
#         <style>
#             body { font-family: Arial; padding: 20px; }
#             table { width: 100%; border-collapse: collapse; }
#             th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
#             th { background-color: #f2f2f2; }
#             img { border: 1px solid #ccc; margin-top: 5px; }
#             pre { background: #f4f4f4; padding: 5px; border-radius: 5px; max-width: 600px; overflow-x: auto; }
#         </style>
#     </head>
#     <body>
#         <h1>📁 Flat File Listing (with JSON & Images)</h1>
#         <table>
#             <tr>
#                 <th>📂 Folder</th>
#                 <th>📄 File</th>
#                 <th>🔍 Preview</th>
#             </tr>
#     """

#     for entry in entries:
#         html += f"<tr><td>{entry['folder']}</td><td>{entry['name']}</td><td>"

#         if "json_data" in entry:
#             html += f"<pre>{json.dumps(entry['json_data'], indent=2)}</pre>"
#         elif entry.get("is_image"):
#             if os.path.exists(entry["full_path"]):
#                 img_url = f"{base_url}/{entry['rel_path']}"
#                 html += f"{base_url}"
#             else:
#                 html += "<span style='color:red;'>❌ Image not found</span>"
#         else:
#             html += "—"

#         html += "</td></tr>"

#     html += "</table></body></html>"

#     return HttpResponse(html)


# import os
# import json
# from django.http import JsonResponse
# from django.conf import settings

# def get_all_files_api(request):
#     base_path = settings.MEDIA_ROOT
#     base_url = settings.MEDIA_URL.rstrip('/')

#     if not os.path.exists(base_path):
#         return JsonResponse({"error": "Base path does not exist."}, status=400)

#     entries = []

#     for root, dirs, files in os.walk(base_path):
#         for file in files:
#             rel_path = os.path.relpath(os.path.join(root, file), base_path).replace("\\", "/")
#             full_path = os.path.join(base_path, rel_path.replace("/", os.sep))
#             file_info = {
#                 "name": file,
#                 "rel_path": rel_path,
#                 "url": f"{base_url}/{rel_path}",
#                 "type": "file",
#                 "folder": os.path.dirname(rel_path).replace("/", " > ") or "Root"
#             }

#             if file.lower().endswith(".json"):
#                 try:
#                     with open(full_path, 'r', encoding='utf-8') as f:
#                         file_info["json_data"] = json.load(f)
#                 except Exception as e:
#                     file_info["json_data"] = f"❌ Error reading JSON: {e}"

#             if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
#                 file_info["is_image"] = True

#             entries.append(file_info)

#     return JsonResponse(entries, safe=False)






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.shortcuts import render
import os
from django.conf import settings
import random
from .models import UserLogin



@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not username or not password or not email:
                return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

            # Create user (no duplicate check, for now)
            UserLogin.objects.create(
                name=username,
                user_pass=password,
                email_address=email
            )

            return JsonResponse({'status': 'success', 'message': 'User created'}, status=201)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'message': 'Only POST allowed'}, status=405)

def members(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            data = json.loads(request.body)
            username = data.get('username')
            password =data.get('password')
            

          

            if not username or not password:
                return JsonResponse({'status': 'error', 'message': 'Username and password required'}, status=400)

            user = authenticate(username=username, password=password)
            if user:
                return JsonResponse({'status': 'success', 'message': 'Login successful'} , status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Only POST requests allowed'}, status=405)







def check_thumbnail_images(request):
    base_dir = settings.MEDIA_ROOT
    data_list = []

    for root, dirs, files in os.walk(base_dir):
        ids = []
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(root, file)
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    image_id = data.get('id')
                    ids.append(str(image_id))
        thumb_folder = os.path.join(root, 'thumbnail')
        images = []
        if os.path.isdir(thumb_folder):
            for img_file in os.listdir(thumb_folder):
                image_path = os.path.join(thumb_folder, img_file)
                rel_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
                image_url = settings.MEDIA_URL + rel_path.replace("\\", "/")
                images.append(image_url)
        if ids or images:
            data_list.append({'ids': ids, 'images': images, 'folder': root})

    if len(data_list) > 4:
        data_list = random.sample(data_list, 4)
   
    return JsonResponse({'all_data': data_list})



