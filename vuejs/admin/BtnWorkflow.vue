<template>
    <v-menu offset-y>
        <template v-slot:activator="{ on }">
            <v-btn :loading="loading" v-on="on" color="primary">{{ state }}</v-btn>
        </template>
        <v-list>
            <v-list-item v-for="(action, idx) in actions" :key="idx" @click="change" :data-value="action">
                <v-list-item-title>{{ action }}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>

<script>
export default {
    props: {
        state: String,
        actions: Array,
        loading: Boolean,
    },

    methods: {
        change(event) {
            this.$emit("menuclick", event.currentTarget.dataset.value)
        },
    },
}
</script>