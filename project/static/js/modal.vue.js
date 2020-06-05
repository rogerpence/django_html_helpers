export function modal() {
    const app = new Vue({
        el: '#app',
        data: {
            visible: false,
            message: '',
            deleteUrl: ''
        },
        methods: {
            showModal(e) {
                const riderId =  e.currentTarget.getAttribute('data-rider-id');
                const riderName = e.currentTarget.getAttribute('data-rider-full-name');

                this.deleteUrl = `rider/${riderId}/delete`;
                this.message = `OK to delete ${riderName}'s account?`;
                this.visible = true;
            },
            closeModal(action) {
                console.log(action);
                if (action === 'yes') {
                    console.log(this.deleteUrl);
                    location.href = this.deleteUrl;
                }

                this.visible = false;
            }
        }
    })
}