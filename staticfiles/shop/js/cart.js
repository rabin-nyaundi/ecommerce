const updateBtns = document.getElementsByClassName('update-cart')

for(let i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        let productId =  this.dataset.product
        let action = this.dataset.action
        console.log('action:', action, 'productId:',productId)

        if (user === 'AnonymousUser') {
            console.log('User not logged in')
        }
        else{
            updateOrder(productId, action)
            console.log(user)
        }
    })
    console.log(user)
}


const updateOrder = (productId, action) =>{

    let url = '/updateItem/'
    
    fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type': 'appliaction/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'productId': productId,
            'action': action,
        })

    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        location.reload()
        console.log('data:', data)
    })


    console.log('Logged in user:', user)
}