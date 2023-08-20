from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Product,Contact,Orders,orderupdate
from .checksum import generateSignature,verifySignature
import json
MERCHANT_KEY='kbzk1DSbJiV_o3p5'
def index(request):
    categories = Product.objects.values('category').distinct()
    allprods = []
    for category in categories:
        products = Product.objects.filter(category=category['category'])
        allprods.append((category['category'], products))
    params = {'prods': allprods}
    return render(request, 'shop/index.html', params)

def product(request,p_id):
    #fetch product using id
    product=Product.objects.filter(product_id=p_id)
    return render(request,'shop/product.html',{'product':product[0]})

def about(request):
    return render(request,'shop/about.html')
def contactus(request):
    if(request.method=="POST"):
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        query=request.POST.get('query','')
        contact=Contact(name=name,email=email,phone=phone,query=query)
        contact.save()
    return render(request,'shop/contactus.html')

def checkout(request):
      thank=False
      id=None
    
      if(request.method=="POST"):
        item_json=request.POST.get('items_json','') 
        amount=request.POST.get('amount','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip','')
        phone=request.POST.get('phone','')
        checkout=Orders(items_json=item_json,amount=amount,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        checkout.save()
        update=orderupdate(order_id=checkout.order_id,update_desc="The Order Has Been Placed")
        update.save()
        thank=True
        id=checkout.order_id
        #request paytm to transfer the amount to your account after payment by user
        param_dict={
            'MID':'WorldP64425807474247',
            'ORDER_ID':str(id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1.8000/handlerequest',
            
        }
        checksum = generateSignature(param_dict,MERCHANT_KEY)
        print("Generated Checksum:", checksum)
        param_dict['CHECKSUMHASH']=checksum
        return render(request,'shop/paytm.html',{'param_dict':param_dict})
      return render(request,'shop/checkout.html',{'thank':thank,'id':id})
  
def tracker(request):
    if(request.method=="POST"):
     verify_id=request.POST.get('verify_orderid',"")
     verify_email=request.POST.get('verify_email',"")
     try:
        check_id = Orders.objects.get(order_id=int(verify_id))
        if check_id.order_id==int(verify_id):
            
            update = orderupdate.objects.filter(order_id=int(verify_id))
            updates = []
            for item in update:
                updates.append({'text': item.update_desc,'time': item.timestamp})
            
            response = json.dumps([updates,check_id.items_json] ,default=str)
            return HttpResponse(response)
        
     except Exception as e:
        return HttpResponse('{}')


    return render(request,'shop/tracker.html')  
@csrf_exempt   
def handlerequest(request):
    pass
    
def searchmatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() :
        return True
    else:
        return False
     

def search(request):
    query = request.GET.get('search')
    allprods = Product.objects.all()
    list_search = []

    for item in allprods:
        if searchmatch(query, item):
            list_search.append(item)

    params = {'prods': list_search}
    return render(request, 'shop/search.html', params)


      