<template>
    <v-card flat class="grey lighten-4">
        <v-card-text v-html="html"></v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        options: [Object, null],
    },
    computed: {
        html() {
            return this.options.html || ""
        },
    },
}
</script>