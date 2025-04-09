from flask import Blueprint, render_template, request
from supabase import create_client
import re
import base64

admin_modify_bp = Blueprint('admin_modify_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_modify_bp.route('/admin_modify', methods=['GET', 'POST'])
def admin_modify():
   if request.method == 'POST':
    try:
        product_name = request.form.get('product_name')
        column = request.form.get('column')
        new_value = request.form.get('new_value')
        image_file = request.files.get('image')

        print("MODIFY POST:", product_name, column, new_value)  # 🔍 For debugging

        if not product_name or not column or not new_value:
            return render_template("error.html", message="✗ Missing required fields.")



            if column not in ['name', 'price', 'description']:
                return render_template("error.html", message="✗ Invalid column selected.")

            # Fetch product ID
            product_res = supabase.table("products").select("id").eq("name", product_name).execute()
            if not product_res.data:
                return render_template("error.html", message="✗ Product not found.")
            product_id = product_res.data[0]['id']

            if column == 'price':
                new_value = float(re.sub(r"[^\d.]", "", new_value))
                if new_value > 99999999.99:
                    return render_template("error.html", message="✗ Price too high (max ₹99999999.99)")

            # Update product field
            supabase.table("products").update({column: new_value}).eq("id", product_id).execute()

            # Optional image upload
            if image_file and image_file.filename:
                binary_data = image_file.read()
                base64_image = base64.b64encode(binary_data).decode('utf-8')
                supabase.table("product_images").insert({
                    "product_id": product_id,
                    "image": base64_image
                }).execute()

            return render_template("success.html", message="✓ Product updated successfully!")

        except Exception as e:
            return render_template("error.html", message=f"✗ Error: {e}")

    else:
        # Handle GET request to pre-fill product name
        product_name = request.args.get('product_name')
        return render_template("admin_modify.html", product_name=product_name)
