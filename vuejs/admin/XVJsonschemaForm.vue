<template>
    <VJsonschemaForm :schema="schema" :model="model" :options="options" @input="input" @error="error" @change="change" >
        <template v-slot:custom-select-from-collection="{modelWrapper, fullKey, fullSchema}">
            <select-from-collection
                :label="fullSchema.title"
                :value="modelWrapper[fullKey]"
                :collectionURL="fullSchema['x-collection-url']"
                @input="modelWrapper[fullKey] = $event" />
        </template>
    </VJsonschemaForm>
</template>
<script>

import VJsonschemaForm from '@koumoul/vjsf'

export default {

    name: 'XVJsonschemaForm',

    components: {
        VJsonschemaForm,
    },

    props: ["model", "schema", "options"],

    methods: {
        error(e) {
            this.$emit("error", e)
        },
        input(e) {
            this.$emit("input", e)
        },
        change(e) {
            this.$emit("change", e)
        },
    },

}
</script>
