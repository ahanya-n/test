from flask import Blueprint, render_template, request
from supabase import create_client

admin_dashboard_bp = Blueprint('admin_dashboard_bp', __name__)

# Supabase config
url = "https://emocnhuvsjfwhyugadiq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVtb2NuaHV2c2pmd2h5dWdhZGlxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4NzU5ODksImV4cCI6MjA1OTQ1MTk4OX0.9RaSAKStvv4x4V1MyIaos92eXu-5FCwN3xJH1BRoyJk"
supabase = create_client(url, key)

@admin_dashboard_bp.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html", products=[])

@admin_dashboard_bp.route('/search_product')
def search_product():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template("admin_dashboard.html", products=[])

    products = supabase.table("products").select("*").ilike("name", f"%{query}%").execute().data or []

    # Fetch one image for each product
    for product in products:
        image_res = supabase.table("product_images").select("image").eq("product_id", product["id"]).limit(1).execute()
        product["image"] = image_res.data[0]["image"] if image_res.data else None

    return render_template("admin_dashboard.html", products=products)
