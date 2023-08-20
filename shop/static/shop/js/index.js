// Find out cart info from local storage
var cart_item, dic_cart, popStr = "";

if (localStorage.getItem('key1')) {
  cart_item = parseInt(localStorage.getItem('key1'));
  dic_cart = JSON.parse(localStorage.getItem('dic_cart'));
  update_cart(dic_cart);
} else {
  cart_item = 0;
  dic_cart = {};
}
update_checkout();
let cart = document.querySelector(".cart");
cart.innerText = "Cart(" + cart_item + ")";

document.getElementById('popoverBtn').addEventListener('click', () => {
  $(document).ready(function () {
    updatepopover(dic_cart); // Update popover content before showing it
    $('#popoverBtn').popover({
      content: popStr,
      placement: 'right',
      trigger: 'focus',
      html: true // Enable HTML interpretation
    });
    $('#popoverBtn').popover('show');
  });
});

// If button is clicked, increment count
function func() {
  var id = event.target.id;
  if (dic_cart[id] !== undefined) {
    dic_cart[id][0]++;
  } else {
    qty=1;
    name=document.getElementById("name"+id).innerHTML;
    price=document.getElementById("price"+id).innerHTML;
    dic_cart[id] = [qty,name,price];
  }
  cart_item++;
  cart.innerText = "Cart(" + cart_item + ")";
  localStorage.setItem('key1', cart_item);
  localStorage.setItem('dic_cart', JSON.stringify(dic_cart));
  console.log(dic_cart);
  update_cart(dic_cart);
  updatepopover(dic_cart);
  update_checkout();
  
}

function update_cart(dic_cart) {
  for (var item in dic_cart) {
    document.getElementById('div' + item).innerHTML = "<button id='minus" + item + "' class='btn btn-primary minus' onclick='minus_func(\"" + item + "\")'><span class='minustext'>-</span></button><span id='val" + item + "' class='itemtext'>" + dic_cart[item][0] + "</span><button id='plus" + item + "' class='btn btn-primary plus' onclick='plus_func(\"" + item + "\")'><span class='plustext'>+</span></button>";
  }
}

function updatepopover(dic_cart) {
  popStr = "<h5>Cart Items:</h5>";
  var i = 1;
  for (var item in dic_cart) {
    popStr += "<b>" + i + "</b>.";
    popStr += document.getElementById('name' + item).innerHTML + " Qty: " + dic_cart[item] + '<br>';
    i++;
  }
}

function minus_func(item) {
  if (dic_cart[item][0] > 1) {
    dic_cart[item][0]--;
    cart_item--;
    cart.innerText = "Cart(" + cart_item + ")";
    update_cart(dic_cart);
  } else {
    document.getElementById('div' + item).innerHTML = "<span id='divpr" + item + "'>" +
      "<button id='" + item + "' class='button-19 btn' onclick='func()'>Add To Cart</button></span>";
    cart_item--;
    cart.innerText = "Cart(" + cart_item + ")";
    delete dic_cart[item];
    
  }
  update_checkout();
  updatepopover(dic_cart);
  localStorage.setItem('key1', cart_item);
  localStorage.setItem('dic_cart', JSON.stringify(dic_cart));
}

function plus_func(item) {
  dic_cart[item][0]++;
  cart_item++;
  cart.innerText = "Cart(" + cart_item + ")";
  update_cart(dic_cart);
  updatepopover(dic_cart);
  update_checkout();
  localStorage.setItem('key1', cart_item);
  localStorage.setItem('dic_cart', JSON.stringify(dic_cart));
}
function update_checkout(){
  let div_btn=document.getElementById("check_out");
  if(cart_item!=0){
    div_btn.innerHTML="<a href='checkout'><button class='btn btn-success'>Checkout</button></a><button class='btn btn-danger mx-2' onclick='clear_cart()'>Clear Cart</button>";
  }
  else{
    div_btn.innerHTML="";
  }
}
function clear_cart() {
for(var item in dic_cart){
  document.getElementById('div' + item).innerHTML = "<span id='divpr" + item + "'>" +
      "<button id='" + item + "' class='button-19 btn' onclick='func()'>Add To Cart</button></span>";
}
localStorage.clear();
cart_item=0;
cart.innerText = "Cart(" + cart_item + ")";
update_checkout();
for (var item in dic_cart){
if(dic_cart.hasOwnProperty(item)){
  delete dic_cart[item];
}
}
}

