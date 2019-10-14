<template>
    <div>
        <div>
            <div>
                <NavigationMenu/>
                <!-- head -->
            </div>
            <ResourceManager />
        </div>
    </div>
</template>
<script>

import ResourceManager from './ResourceManager.vue'
import NavigationMenu from './NavigationMenu.vue'
import { mapGetters } from 'vuex'

function decodeRoute(route) {
    const routePath = route.path.replace(/(^[/]*)|([/]*$)/g, '')
    const path = [""];
    for (let part of routePath.split('/')) {
        if (part !== "") {
            part = decodeURIComponent(part)
            path.push(part)
        }
    }
    const view = route.query.view || "main"
    return {
        path: path,
        view: "main",
    }
}

export default {

    computed: {
        ...mapGetters([
            'user_email',
        ])
    },
    components: {
        NavigationMenu,
        ResourceManager,
    },

    watch: {
        '$route' (to, from) {
            const opts = decodeRoute(to)
            this.$store.dispatch('changeResource', opts)
            this.$store.dispatch('changeView', opts)
        },

        user_email(to) {
            if(to && (this.$store.state.path !== null)) {
                const opts = decodeRoute(this.$route)
                this.$store.dispatch('changeResource', opts)
                this.$store.dispatch('changeView', opts)
            }
        },
    },

    mounted() {
        this.$store.dispatch('connect', {baseURL: '/api/'})
    },
}


</script>
<style lang="sass">

@import url('https://fonts.googleapis.com/css?family=Playfair+Display|Source+Sans+Pro&display=swap');

html
body
    margin: 0
    padding: 0
    font-family: 'Source Sans Pro', sans-serif

</style>


