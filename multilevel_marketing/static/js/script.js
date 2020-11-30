// document.addEventListener("DOMContentLoaded", function(){
//     var modal = document.getElementById("myModal");
//     var display_imgs = document.getElementsByClassName("display_img")
//     var span = document.getElementsByClassName("close")[0];
//     var add_item_buttons = document.getElementsByClassName("add_item_button");

//     for(i = 0; i < display_imgs.length; i++){
//         display_imgs[i].onclick = function() {
//             modal.style.display = "block";
//             console.log(this.getAttribute('product_id'));
//             fetch('/details/'+this.getAttribute('product_id'))
//                 .then(data => data.json())
//                 .then(data => {
//                     console.log(data)
//                     span.innerHTML =`
//                     <p>Name: ${data.name}</p>
//                     <p>Price: ${data.price}</p>
//                     <p>Description ${data.desc}</p>
//                     <img src="../static/pictures/${data.image}">
//                     `
//                 })
//         }
//     }

//     for(i = 0; i < add_item_buttons.length; i++) {
//         add_item_buttons[i].onclick = function() {
//             prod_id = this.getAttribute('product_id')
//             amount = document.getElementById('add_item_selection_'+prod_id).value;
//             fetch('/add_item/'+prod_id+'/'+amount)
//                 .then(data => data.json())
//                 .then(data => {
//                     console.log(data)
//                     document.getElementById('cart_item_count').innerHTML = data.items_in_cart
//                 })
//         }
//     }

//     // for(i = 0; i < add_item_buttons.length; i++) {
//     //     add_item_buttons[i].onclick = function() {
//     //         prod_id = this.getAttribute('product_id')
//     //         amount = document.getElementById('add_item_selection_'+prod_id).value;
//     //         fetch('/add_item/'+prod_id+'/'+amount)
//     //             .then(data => data.json())
//     //             .then(data => {
//     //                 console.log(data)
//     //                 document.getElementById('cart_item_count').innerHTML = data.items_in_cart
//     //             })
//     //     }
//     // }

//     span.onclick = function() {
//         modal.style.display = "none";
//     }
//     window.onclick = function(event) {
//         if (event.target == modal) {
//             modal.style.display = "none";
//         }
//     }
// })




// if (localStorage.getItem('cart') == null) {
//     var cart = {};
// } else {
//     cart = JSON.parse(localStorage.getItem('cart'));
//     // updateCart(cart);
// }


// document.addEventListener("DOMContentLoaded", function(){
//     var modal = document.getElementById("myModal");
//     var display_imgs = document.getElementsByClassName("display_img")
//     var span = document.getElementsByClassName("close")[0];
//     var add_item_buttons = document.getElementsByClassName("add_item_button");

//     for(i = 0; i < display_imgs.length; i++){
//         display_imgs[i].onclick = function() {
//             modal.style.display = "block";
//             console.log(this.getAttribute('product_id'));
//             fetch('/details/'+this.getAttribute('product_id'))
//                 .then(data => data.json())
//                 .then(data => {
//                     console.log(data)
//                     span.innerHTML =`
//                     <p>Name: ${data.name}</p>
//                     <p>Price: ${data.price}</p>
//                     <p>Description ${data.desc}</p>
//                     <img src="../static/pictures/${data.image}">
//                     `
//                 })
//         }
//     }

//     for(i = 0; i < add_item_buttons.length; i++) {
//         add_item_buttons[i].onclick = function() {
//             prod_id = this.getAttribute('product_id')
//             amount = document.getElementById('add_item_selection_'+prod_id).value;
//             fetch('/add_item/'+prod_id+'/'+amount)
//                 .then(data => data.json())
//                 .then(data => {
//                     console.log(data)
//                     document.getElementById('cart_item_count').innerHTML = data.items_in_cart
//                 })
//         }
//     }




// $('#checkout').on('click', function(){
    
//     localStorage.clear();
//     cart = {};
//     updateCart(cart);
// });


if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
        // updateCart(cart);
}
     

// If the add to cart button is clicked, add/increment the item
//$('.cart').click(function() {
    $('.divpr').on('click', 'button.cart', function(){
        
    var idstr = this.id.toString();
   if (cart[idstr] != undefined) {
       
        qty = cart[idstr][0] + 1;
    } else {
        
        qty = 1;
        id=document.getElementById('Product_id'+idstr).innerHTML;
        img=document.getElementById('Product_img'+idstr).innerHTML;
       
        Product_Name = document.getElementById('Product_Name'+idstr).innerHTML;
        // Product_Size = document.getElementById('Product_Size'+idstr).innerHTML;
        Price = document.getElementById('Price'+idstr).innerHTML;
        Courier = document.getElementById('Courier'+idstr).innerHTML;
        cart[idstr] = [qty, Product_Name,parseInt(Price),id,img,parseInt(Courier)];
        
    }
   
    updateCart(cart);
    
});
$('.icon-pencil').on('click', 'button.cart', function(){
    var idstr = this.id.toString();
   if (cart[idstr] != undefined) {
       
        qty = cart[idstr][0] + 1;
    } else {
        
        qty = 1;
        id=document.getElementById('Product_id'+idstr).innerHTML;
        
        img=document.getElementById('Product_img'+idstr).innerHTML;
        Product_Name = document.getElementById('Product_Name'+idstr).innerHTML;
        // Product_Size = document.getElementById('Product_Size'+idstr).innerHTML;
        // console.log(Product_Size);
        Price = document.getElementById('Price'+idstr).innerHTML;       
        Courier = document.getElementById('Courier'+idstr).innerHTML;
        cart[idstr] = [qty, Product_Name,parseInt(Price),id,img,parseInt(Courier)];
        
    }
   
    updateCart(cart);
    
});
//Add Popover to cart
$('#popcart').popover();
updatePopover(cart);

function updatePopover(cart) {
    var popStr = "";
    popStr = popStr + '';
    var i = 1;
    var total=0;
    var checkout='';
    var count=0;
    var cart_view='';
    
    for (var item in cart) {
        count=count+cart[item][0];
        popStr=popStr+'<div class="minicart-prd"><div class="minicart-prd-image"><a href=""><img class="lazyload" alt="" src="'+cart[item][4]+'"></a></div><div class="minicart-prd-name"><h5><a href="#">canverse</a></h5><h2><a href="#">'+ cart[item][1] +'</a></h2></div><div class="minicart-prd-qty"><span>qty:</span> ';
        popStr=popStr+'<b>'+cart[item][0]+'</b></div>  <div class="minicart-prd-qty"><span>Courier:</span>  <b>'+cart[item][5]+'</b></div><div class="minicart-prd-price"><span>price:</span> ';
        popStr=popStr+'<b>&#8377;'+cart[item][2]*cart[item][0]+'</b></div><div class="minicart-prd-action"><a href="#" class="icon-heart js-label-wishlist"></a>  <a class="icon-cross delete-from-wishlist" onclick="clearCart(this.id);" id ="'+item+'"></a> </div></div>';
        total=total+(cart[item][2]*cart[item][0])+parseInt(cart[item][5])
        checkout=checkout+'<div class="cart-table-prd"><div class="cart-table-prd-image"><a href="#"><img src="'+cart[item][4]+'" alt=""></a></div><div class="cart-table-prd-name"><h2><a href="#">'+ cart[item][1] +'</a></h2></div><div class="cart-table-prd-price"><b>&#8377; '+ cart[item][5] +'</b></div><div class="cart-table-prd-qty"><b>'+ cart[item][0] +'</b></div><div class="cart-table-prd-price"><b>&#8377; '+ cart[item][2]*cart[item][0] +'</b></div></div>';
        // cart_view=cart_view+'<div class="cart-table-prd"><div class="cart-table-prd-image"><a href="#"><img src="'+cart[item][4]+'" alt=""></a></div><div class="cart-table-prd-name"><h5><a href="#">canverse</a></h5><h2><a href="#">'+ cart[item][1] +'</a></h2></div><div class="cart-table-prd-qty"><span>qty:</span> <b>'+cart[item][0]+'</b></div><div class="cart-table-prd-price"><span>price:</span> <b>&#8377; '+ cart[item][2]*cart[item][0] +'</b></div><div class="cart-table-prd-action"><a href="#" class="icon-heart"></a> <a href="#" class="icon-pencil"></a> <a href="#" class="icon-cross"  onclick="clearCart(this.id);" id ="'+item+'"></a></div></div>'
    }
    $('#aaa').html(popStr);
    $('#amount').html(total);
    total='&#8377; '+total;
    $('#total').html(total);
    $('#total1').html(total);
   
    $('#check').html(checkout);
    $('#cart').html(count);
    $('#cart_view').html(cart_view);
    $('#itemsJson').val(JSON.stringify(cart));
    $('#itemsJson1').val(JSON.stringify(cart));
    $('#products_id').val(JSON.stringify(cart));
    
}

function clearCart(clicked_id) {

    cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        if(item==clicked_id)
        {
        
        document.getElementById('div' + cart[item][3]).innerHTML = '<button id="' + item + '" class="btn btn-primary cart">AddTo Cart</button>'
        }
    }
        
    delete cart[clicked_id];
    
    updateCart(cart);
}

function updateCart(cart) {
   
    var sum = 0;
    for (var item in cart) {
        console.log(document.getElementById("div" + cart[item][3]));
        if(document.getElementById("div" + cart[item][3])!=null)
        {
           
            sum = sum + cart[item][0];
            document.getElementById("div" + cart[item][3]).innerHTML =   "<button id='minus" + item + "' class='btn btn-primary minus'>-</button> &nbsp; <span id='val" + item + "''>"+ " " + cart[item][0] + " "  + "</span> &nbsp; <button id='plus" + item + "' class='btn btn-primary plus'> + </button>";
        }
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = sum;
    updatePopover(cart);
}
function clearAll() {
    cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        document.getElementById('div' + cart[item][3]).innerHTML = '<button id="' + item + '" class="btn btn-primary cart">AddTo Cart</button>'
    }
    localStorage.clear();
    cart = {};
    updateCart(cart);


}
// If plus or minus button is clicked, change the cart as well as the display value
$('.divpr').on("click", "button.minus", function() {
    
    a = this.id.slice(7, );
    cart['pr' + a][0] = cart['pr' + a][0] - 1;
    cart['pr' + a][0] = Math.max(0, cart['pr' + a][0]);
    if (cart['pr' + a][0] == 0){
        document.getElementById('div' + a).innerHTML = '<button id="pr'+a+'" class="btn btn-primary cart">AddTo Cart</button>';
        delete cart['pr'+a];
    }
    else{
        document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    }
    updateCart(cart);
    

});

$('.divpr').on("click", "button.plus", function() {
    a = this.id.slice(6, );
    cart['pr' + a][0] = cart['pr' + a][0] + 1;
    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    updateCart(cart);
});


$(function() {
    var chk = $('#checkbox1');
    var btn = $('#create');
  
    chk.on('change', function() {
      btn.prop("disabled", !this.checked);//true: disabled, false: enabled
    }).trigger('change'); //page load trigger event
  });