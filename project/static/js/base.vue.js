export function base() {
    const app = new Vue({
        el: '#base-app',
        data: {
        },
        mounted() {
        },
        methods: {
            toggleNav(e) {
                const mainNav = document.getElementById('main-nav');
                console.log('clicked');
                mainNav.classList.toggle('hidden');
            },
        }
    })
}