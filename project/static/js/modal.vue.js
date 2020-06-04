export function modal() {
    const app = new Vue({
        el: '#app',
        data: {
            visible: false,
            deleteAction: 'delete-rider.html',
            message: 'OK to delete<br> Neil Young\'s account?',
            currentAction: '',
            currentRow: 0
        },
        methods: {
            showModal(e) {
                this.currentAction = e.currentTarget.getAttribute('data-action');
                this.currentRow = e.currentTarget.getAttribute('data-row-number');
                console.log(this.currentAction);
                console.log(this.currentRow);
                this.visible = true;
            },
            closeModal(e) {
                console.log(this.currentAction);
                this.visible = false;

                // name = document.querySelector('span[data-rider-name="1"]');
                // riderName = name.innerText

                // if (confirm == 'yes') {
                //     console.log('deleted selected');
                //     // location.href = this.deleteAction;
                // }
                // else {
                //     console.log('delete not selected');
                // }
            }
        }
    })
}