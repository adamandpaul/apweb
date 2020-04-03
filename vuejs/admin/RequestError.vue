<template>
    <div class="request-view">
        <h1>Request Error</h1>

        <template v-if="request">
            <template v-if="config">
                <p>{{ config.method.toUpperCase() }} {{ config.url }}</p>
            </template>

            <template v-if="response">
                <p>{{ serverTimestamp}}</p>
                <p>Server responded with an error {{ serverCode }}</p>
                <p>{{serverMessage}}</p>
                <pre v-for="(line, idx) in serverException" :key="'a' + idx">{{ line }}</pre>
                <pre v-for="(line, idx) in serverTraceback" :key="'b' + idx">{{ line }}</pre>
            </template>

            <template v-else>
                <p>A request was made but no response was received.</p>
                <pre>{{ error.message }}</pre>
            </template>
        </template>
        <template v-else>
            <p>The was an error in forming a request</p>
            <pre>{{ error.message }}</pre>
        </template>

    </div>
</template>
<script>
export default {

    props: {
        error: {
            defatul: {},
        },
    },

    computed: {
        request() {return this.error.request},
        response() {return this.error.response},
        config() {return this.error.config},

        serverTimestamp() {return this.response.data.timestamp},
        serverMessage() {return this.response.data.message},
        serverCode() {return this.response.data.code},
        serverData() {return this.response.data.data},
        serverException() {return this.response.data.exception || []},
        serverTraceback() {return this.response.data.traceback || []},
    },

}
</script>
<style lang="sass" scoped>

</style>
