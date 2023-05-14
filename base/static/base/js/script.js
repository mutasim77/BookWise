import { blogs } from "./constant.js";

//? that i'm using single .js file for multiple .html templates, I'll check path and run codes for specific page;
const pathName = (document.location).pathname.replaceAll("/", '');

switch (pathName) {
    //! MAIN PAGE
    case "":
        //! Blogs
        const divBlogs = document.querySelector('#blogs');

        for (let i = 2; i < blogs.length; i++) {
            divBlogs.innerHTML +=

                `
                <div class="col-md-4 col-sm-12">
                    <img src='${blogs[i].img}'>
                    <div class="d-flex gap-4 mt-3">
                        <h5> <i class="fa fa-user" aria-hidden="true"></i> ${blogs[i].publisher}</h5>
                        <h5> <i class="fa fa-calendar" aria-hidden="true"></i> ${blogs[i].date}</h5>
                    </div>
                    <h3 class="mt-3 fs-5 fw-bold">${reduceText(blogs[i].title, 5)}</h3>
                    <p>
                        ${reduceText(blogs[i].description, 20)}
                    </p>
                    <a href="/blog/" class="btn btn-danger mb-3">Read More</a>
                </div>
            `
        }

        function reduceText(text, num) {
            return text.split(' ').slice(0, num).join(' ');
        }

        //! Search Bar
        const searchButton = document.querySelector("#search-btn");
        const searchCloseButton = document.querySelector("#search-close-btn");

        //?search button
        searchButton.addEventListener('click', () => {
            open('.search-bar')
        });

        //?close search button
        searchCloseButton.addEventListener('click', () => {
            close('.search-bar')
        });

        //! CART
        const cartButton = document.querySelector('#cart-btn');
        const cartCloseButton = document.querySelector('#cart-close-btn');

        //? open cart
        cartButton.addEventListener('click', () => {
            open('#cart');
            getFromLocalStorage();
            updateTotal();
        })

        //? close cart 
        cartCloseButton.addEventListener('click', () => {
            close('#cart');
        });

        //* Helper functions
        function open(selector) {
            document.querySelector(selector).classList.add('show');
            document.querySelector('#modal').classList.add('show');
            document.querySelector('body').classList.add('hidden');
        }

        function close(selector) {
            document.querySelector(selector).classList.remove('show');
            document.querySelector('#modal').classList.remove('show');
            document.querySelector('body').classList.remove('hidden');
        }

        //? ADD TO CART BUTTON
        const buttonAddToCart = document.querySelectorAll('#add-cart-btn');
        buttonAddToCart.forEach((button) => {
            button.addEventListener('click', (event) => {
                const parentElement = event.target.parentElement;
                const bookImage = (parentElement.querySelector('img').src).substring(21, (parentElement.querySelector('img').src).length);
                const bookTitle = (parentElement.querySelector('img').alt);
                const bookPrice = (parentElement.querySelector('#price').textContent).split('$')[1];
                const bookAuthor = (parentElement.querySelector('#book-author').textContent)

                const objBookInfo = {
                    image: bookImage,
                    title: bookTitle,
                    price: bookPrice,
                    author: bookAuthor
                }

                event.target.classList.add('show');

                setTimeout(() => {
                    event.target.classList.remove('show');
                }, 500)

                setToLocalStorage([objBookInfo]);
            })
        })

        //! Take data from books and store them in localStorage
        function setToLocalStorage(data) {
            const username = (document.querySelector("[data-username]").dataset.username);

            if (localStorage.getItem(username)) {
                let cart = JSON.parse(localStorage.getItem(username));
                const hasItem = cart.some(item => item.title === data[0].title);
                if (!hasItem) {
                    cart.push(data);
                }
                cart = cart.flat()
                localStorage.setItem(username, JSON.stringify(cart))
            } else {
                localStorage.setItem(username, JSON.stringify(data));
            }


        }

        //! Get data from localStorage and show it in CART
        function getFromLocalStorage() {
            const username = (document.querySelector('[data-username]').dataset.username);
            const data = JSON.parse(localStorage.getItem(username));
            const cartItems = document.querySelector('.cart-items');

            if (!username) {
                console.log('hello');
            }

            if (!data.length) {
                cartItems.innerHTML = `<span class="d-flex justify-content-center py-3 fs-5 text-body-secondary fst-italic fw-bold">No items in cart</span>`
                return
            }

            cartItems.innerHTML = ''

            for (const book of data) {

                cartItems.innerHTML +=
                    `
                   <div class="d-flex gap-4">
                        <img src="${book.image}" alt="${book.title}" class="w-25 h-25 rounded">
                        <div class="info w-100 d-flex flex-column gap-2 align-items-start">
                            <h2 class="fs-6 fw-bold">${reduceText(book.title, 5)}</h2>
                            <h4 class="text-body-tertiary"><i class="fa-solid fa-user-pen"></i> ${book.author}</h4>
                            <div class="d-flex w-100 justify-content-between align-items-center">
                                <span class="fs-5 text-danger-emphasis">$${book.price}</span>
                                <i class="fa fa-trash bg-danger p-2 text-white rounded-2 mx-5" id="trash-btn" role="button"></i>
                            </div>
                        </div>
                    </div>
                    <hr>
                `
            }

            removeFromLocalStorage();
        }


        //! Remove data from localStorage;
        function removeFromLocalStorage() {
            const username = (document.querySelector('[data-username]').dataset.username);
            const trashButtons = document.querySelectorAll('#trash-btn');

            trashButtons.forEach(btn => {
                btn.addEventListener('click', (event) => {
                    const parentElement = event.target.parentElement.parentElement.parentElement;
                    const hrLine = parentElement.nextElementSibling;
                    const bookTitle = parentElement.querySelector('img').alt;

                    //? Delete from DOM;
                    parentElement.remove();
                    hrLine.remove();

                    //? Delete from localStorage
                    let data = JSON.parse(localStorage.getItem(username));
                    data = data.filter(item => item.title !== bookTitle);
                    localStorage.setItem(username, JSON.stringify(data));

                    updateTotal();
                })
            })


        }

        function updateTotal() {
            const username = document.querySelector('[data-username]').dataset.username;
            const totalDivPrice = document.querySelector('#total-price');

            const data = JSON.parse(localStorage.getItem(username))
            const total = data.reduce((total, curr) => +total + +curr.price, 0);

            if (!total) {
                const cartItems = document.querySelector('.cart-items');
                cartItems.innerHTML = `<span class="d-flex justify-content-center py-3 fs-5 text-body-secondary fst-italic fw-bold">- No items in cart -</span>`
            }

            totalDivPrice.innerHTML = `<span class="fw-bold">Total: </span> $${total.toFixed(2)}`
        }

        break;

    //! BLOG PAGE
    case "blog":
        //! Fetch the Data from API FOR QUOTE
        async function getQuotes(url) {
            const res = await fetch(url);
            const quotes = await res.json();
            show(quotes);
        }

        getQuotes("https://type.fit/api/quotes");

        let counter = 0;
        function show(quotes) {
            let arr = quotes;
            const button = document.querySelector('.quotes button');

            button.addEventListener('click', () => {
                document.querySelector('.quotes q').textContent = arr[++counter].text;
            })
        }

        break;

    default:
        break;
}
