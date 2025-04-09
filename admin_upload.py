from flask import Blueprint, request, render_template
from supabase import create_client
import re
import base64

admin_upload_bp = Blueprint('admin_upload_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_upload_bp.route('/upload-product')
def upload_product():
    return render_template("admin_upload.html")

@admin_upload_bp.route('/upload', methods=['POST'])
def upload():
    try:
        name = request.form.get('product_title')
        raw_price = request.form.get('price')
        description = request.form.get('description')
        images = request.files.getlist('images')

        price = float(re.sub(r"[^\d.]", "", raw_price))

        product_data = {
            "name": name,
            "price": price,
            "description": description
        }

        product_response = supabase.table("products").insert(product_data).execute()
        if not product_response.data:
            return render_template("error.html", message="✗ Failed to insert product!")

        product_id = product_response.data[0]['id']

        for img in images:
            if img and img.filename:
                binary_data = img.read()
                base64_image = base64.b64encode(binary_data).decode('utf-8')
                image_record = {
                    "product_id": product_id,
                    "image": base64_image
                }
                supabase.table("product_images").insert(image_record).execute()

        return render_template("success.html", message="✓ Product and images uploaded successfully!")

    except Exception as e:
        return render_template("error.html", message=f"✗ Error: {e}")
