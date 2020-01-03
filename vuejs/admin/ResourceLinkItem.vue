<template>
    <v-btn
        class="link"
        :href="url"
        elevation="0"
        :color="color"
        :dark="dark"
        >
        <v-icon class="mr-2">link</v-icon>
        {{ title }}
    </v-btn>
</template>
<script>

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
        url() { return this.item.url },
        color() {
            if (this.dark) {
                return "teal"
            } else {
                return "teal lighten-5"
            }
        }
    },

}
</script>
<style lang="sass" scoped>

.link
    margin-right: 8px
    margin-top: 6px

</style>
