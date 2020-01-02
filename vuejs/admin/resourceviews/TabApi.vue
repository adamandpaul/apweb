<template>
    <div>
        <v-form ref="form" v-model="valid" @submit.prevent="execute">
            <v-card flat>
                <v-card-title>{{ title }}</v-card-title>
                <v-card-text>
                    <v-jsonschema-form v-if="schema" :schema="schema" :model="input" :options="formOptions"/>
                    <v-alert v-if="error" type="error" text>
                        {{ error }}
                    </v-alert>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="clear">Clear</v-btn>
                    <v-btn :disabled="inProgress" color="primary" @click="execute">{{ executeText }}</v-btn>
                </v-card-actions>
                <v-progress-linear
                    :active="inProgress"
                    :indeterminate="inProgress"
                    absolute
                    bottom
                    ></v-progress-linear>
            </v-card>
        </v-form>
        <div v-if="currentResult">
            <v-card class="my-4">
                <v-card-text>
                    <pre>{{ JSON.stringify(currentResult, null, 2) }}</pre>
                </v-card-text>
            </v-card>
        </div>
        <request-error v-if="requestError" :error="requestError" />
    </div>
</template>
<script>

import {mapGetters} from 'vuex'

export default {

    props: {
        title: String,
        data: [Object, null],
        options: [Object, null]
    },

    data() {
        return {
            valid: false,
            formOptions: {
                debug: false,
                disableAll: false,
                autoFoldObjects: false,
            },
            error: null,
            requestError: null,
            input: {},
            inProgress: false,
            currentInput: null,
            currentResult: null,
        }
    },

    computed: {
        ...mapGetters([
            'resourceApi',
        ]),
        schema() {
            return this.data || this.options.schema
        },
        api() {
            return this.options.api
        },
        method() {
            return this.options.method || "get"
        },
        executeText() {
            if (this.options.executeText) {
                return this.options.executeText
            } else if (this.method == "get") {
                return "Query"
            } else {
                return "Commit"
            }
        },
    },

    methods: {
        execute() {
            if (!this.valid) {
                this.error = "The form did not validate, please check the fields above"
                return
            }
            this.error = null
            this.requestError = null
            this.currentResult = null
            this.currentInput = {...this.input}
            this.inProgress = true

            let promise = null
            if (this.method == "get") {
                promise = this.resourceApi.get(this.api, {
                    params: this.currentInput,
                })
            } else {
                promise = this.resourceApi({
                    method: this.method,
                    url: this.api,
                    data: this.currentInput,
                })
            }
            promise.then(this.handleResponse).catch(this.handleError)
        },
        clear() {
            for (let key in this.input) {
                this.input[key] = null
            }
            this.error = null
            this.$refs.form.reset()
        },
        handleResponse(resp) {
            this.currentResult = resp.data.data
            this.inProgress = false
        },
        handleError(err) {
            this.inProgress = false
            this.requestError = err
        },
    },
}

</script>
