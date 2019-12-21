<template>
    <div>
        <v-form ref="form" v-model="valid" @submit.prevent="add" :update-key="updateKey">
            <v-card>
                <v-card-title>{{ this.schema.title }}</v-card-title>
                <v-card-text>
                    <v-jsonschema-form v-if="schema" :schema="schema" :model="value" :options="formOptions" @error="showError" @input="input"/>
                    <v-alert v-if="error" type="error" text>
                        {{ error }}
                    </v-alert>
                    <v-alert v-if="saved" type="success" text>
                        Saved
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn :loading="inProgress" color="primary" @click="save">Save</v-btn>
                </v-card-actions>
            </v-card>
        </v-form>
        <template v-if="requestError">
            <request-error :error="requestError" />
        </template>
    </div>
</template>
<script>

import ResourceMenu from '../ResourceMenu.vue'
import {mapGetters} from 'vuex'

export default {

    props: {
        data: [Object, null],
        options: [Object, null],
    },

    data() {
        return {
            value: {},
            updateKey: 0,
            valid: false,
            error: null,
            requestError: null,
            formOptions: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            inProgress: false,
            saved: false,
        }
    },
    computed: {
        ...mapGetters([
            'resourceApi',
        ]),
        schema() {
            return this.data || this.options.schema
        }
    },

    methods: {
        input() {
            this.saved = false
        },
        showError(err) {
            this.error = err
        },
        save() {
            if (!this.valid) {
                this.showError("The form did not validate, please check the fields above")
                return
            }
            this.inProgress = true
            this.resourceApi.patch('', this.value)
                .then(this.handleResponse)
                .catch(this.handleError)
        },
        clear() {
            for (let key in this.value) {
                this.value[key] = null
            }
            this.error = null
            this.requestError = null
            this.$refs.form.reset()
        },
        handleResponse(resp) {
            this.inProgress = false
            this.saved = true
            this.$root.$emit("resourceUpdated")
        },
        handleError(err) {
            this.inProgress = false
            this.requestError = err
        },
    }

}
</script>
