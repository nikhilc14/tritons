burger = document.querySelector('.burger')
navbar = document.querySelector('.navbar')
navlist = document.querySelector('.nav-list')
rightnav = document.querySelector('.Right-nav')
contact = document.querySelector('.form')
searchbar = document.querySelector('.btn-sm')

burger.addEventListener('click',()=>{

    rightnav.classList.toggle('v-class-resp');
    navlist.classList.toggle('v-class-resp');
    navbar.classList.toggle('h-nav-resp');

})

contact.addEventListener('click',function(){
    alert('Please send a mail to this mail id example@gmail.com');
});

searchbar.addEventListener('click',function(){
    let input = document.querySelector('imput');

    if(input.value.toLowerCase() == 'home'){
        window.location ='index.html';
    }
    else if(input.value.toLowerCase() == 'innovation'){
        window.location ='innovation.html';
    }
    else if(input.value.toLowerCase() == 'products'){
        window.location ='products.html';
    }
    else if(input.value.toLowerCase() == 'about us'){
        window.location ='aboutus.html';
    }
    else{
        alert('ERROR: The page which you are trying to visit is not available on our website');
    }

});


