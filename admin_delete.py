from flask import Blueprint, render_template, request
from supabase import create_client

admin_delete_bp = Blueprint('admin_delete_bp', __name__)

url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"  # ← Replace with your real Supabase key
supabase = create_client(url, key)

@admin_delete_bp.route('/delete-product', methods=['POST', 'GET'])
def delete_product():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            try:
                result = supabase.table("products").select("id").eq("name", product_name).execute()
                if not result.data:
                    return render_template("error.html", message="✗ Product not found.")

                product_id = result.data[0]['id']
                supabase.table("products").delete().eq("id", product_id).execute()
                return render_template("success.html", message="✓ Product deleted successfully!")
            except Exception as e:
                return render_template("error.html", message=f"✗ Error: {e}")
        else:
            return render_template("error.html", message="✗ Product name not provided.")
    return render_template("admin_delete.html")
