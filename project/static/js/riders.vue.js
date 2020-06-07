export function modal() {
    const app = new Vue({
        el: '#app',
        data: {
            visible: false,
            message: '',
            deleteUrl: '',
            riderId: '',
        },
        mounted() {
            this.showFlashMessage()
        },
        methods: {
            clearSearch(e) {
                console.log(e);
                const searchInput = document.getElementById('search');
                searchInput.value = '';
                document.getElementById('search-form').submit();
            },
            showFlashMessage() {
                const messages = document.querySelectorAll('.django-message');
                let messageTop = 0;
                messages.forEach((message, i)=> {
                    message.style.top = `${messageTop}px`;
                    messageTop +=60;

                    setTimeout(()=>{
                        message.classList.add('fade-in');
                    },300);

                    // // }, 300)
                    setTimeout(() => {
                        message.classList.remove('fade-in');
                        message.classList.add('fade-out');
                    }, 3000)

                })
            },
        }
    })
}