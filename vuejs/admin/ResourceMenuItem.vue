<template>
    <v-btn
        class="router-link"
        :to="routeTo"
        elevation="0"
        :color="color"
        :dark="dark"
        >
        {{ title }}
    </v-btn>
</template>
<script>

import utils from '../utils'

export default {

    props: {
        item: Object,
        dark: {
            type: Boolean,
            default: false,
        }
    },

    computed: {
        title() { return this.item.title },
        routeTo() { return this.pathToString(this.item.path) },
        color() {
            if (this.dark) {
                return "blue-grey"
            } else {
                return "blue-grey lighten-5"
            }
        }
    },

    methods: {
        pathToString: utils.pathToString,
    },
}
</script>
<style lang="sass" scoped>

.router-link
    margin-right: 8px
    margin-top: 6px

</style>
