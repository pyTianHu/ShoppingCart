from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.Certificate(r"C:\Users\Felhasználó\AppData\Local\Programs\Python\Python312\Projects\shoppingcart_pk.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def home(request):

    return render(request, "index.html")

# Create your views here.
@csrf_exempt
def add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_category = request.POST.get('product_category')
        store = request.POST.get('store')
        price_huf = int(request.POST.get('price_huf'))
        size = int(request.POST.get('size'))
        size_uom = request.POST.get('size_uom')
        unit_price_huf = int(request.POST.get('unit_price_huf'))
        unit_price_uom = request.POST.get('unit_price_uom')
        for_sale = request.POST.get('for_sale') == 'on'

        data = {
            'product_name': product_name,
            'product_category': product_category,
            'store': store,
            'price_huf': price_huf,
            'size': size,
            'size_uom': size_uom,
            'unit_price_huf': unit_price_huf,
            'unit_price_uom': unit_price_uom,
            'for_sale': for_sale
        }

        # Generate a custom document ID if needed, otherwise Firestore will auto-generate one
        custom_doc_id = f"{product_name}_{datetime.datetime.now().strftime('%Y%m%d')}_{store}"

        doc_ref = db.collection('products').document(custom_doc_id)
        doc_ref.set(data)
        
        return redirect('home')
    else:
        return render(request, "add.html")