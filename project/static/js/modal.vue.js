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
            showModal(e) {
                this.riderId =  e.currentTarget.getAttribute('data-rider-id');
                const riderName = e.currentTarget.getAttribute('data-rider-full-name');

                this.deleteUrl = `/riders/${this.riderId}/delete/`;
                this.message = `OK to delete ${riderName}'s account?`;
                this.visible = true;
            },
            closeModal(action) {
                console.log(action);
                if (action === 'yes') {
                    console.log(this.deleteUrl);
                    // location.href = this.deleteUrl;
                }

                this.visible = false;
            }
        }
    })
}