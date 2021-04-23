var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
        var  pharmacy= this.dataset.pharmacy
		console.log('productId:', productId, 'Action:', action,"Pharmacy:",pharmacy)

        console.log('USER:', user)
		if (user == 'AnonymousUser'){
			console.log('User is not authenticated');
            addCookieItem(productId, action, pharmacy);
			
		}else{
			updateUserOrder(productId, action,pharmacy);
		}

	})
}


function updateUserOrder(productId, action,pharmacy){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action,'pharmacy':pharmacy})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data);
            location.reload();
		});
}



function addCookieItem(productId, action, pharmacy){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[pharmacy] == undefined){
            cart[pharmacy] ={}
		    cart[pharmacy][productId] = {'quantity':1}

		}
        else if(cart[pharmacy][productId]==undefined){
            cart[pharmacy][productId] = {'quantity':1}

        }
        else{
			cart[pharmacy][productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[pharmacy][productId]['quantity'] -= 1

		if (cart[pharmacy][productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[pharmacy][productId];
		}
        else if(cart[pharmacy]== {}){
            delete cart[pharmacy]
        }
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}
