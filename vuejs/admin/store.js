
import axios from 'axios'

const DEFAULT_ROOT_NAVIGATION_NODE = {
    "title": "App",
    "path": [""],
    "named_resources": [],
}

export default {

    state: {
        path: null,
        view: "main",
        loading: true,
        error: null,
        breadcrumbs: [DEFAULT_ROOT_NAVIGATION_NODE],
        rootNavigationNode: DEFAULT_ROOT_NAVIGATION_NODE,
    },

    mutations: {
        loadingStart(state, path) {
            state.path = path
            state.loading = true
            state.error = null

            // reset current workspace state
            state.breadcrumbs = [state.rootNavigationNode]
        },
        loadingComplete(state, data) {
            state.loading = false
            state.error = null

            // set workspace state
            state.breadcrumbs = data.breadcrumbs

            // Save root navigation node
            state.rootNavigationNode = state.breadcrumbs[0]
        },
        loadingError(state, error) {
            state.loading = false
            state.error = error
        },
        setView(state, view) {
            state.view = view
        },
    },

    actions: {
        loadResource(context, opts) {
            context.commit('loadingStart', opts.path)
            context.getters.resourceApi.get("@@view-admin")
            .then((resp) => {
                context.commit("loadingComplete", resp.data.data)
            }).catch((error) => {
                context.commit("loadingError", error)
            })
        },
        changeResource(context, opts) {
            if (context.getters.path !== opts.path) {
                context.dispatch("loadResource", opts)
            }
        },
        changeView(context, opts) {
            context.commit('setView', opts.view)
        },
    },

    getters: {
        path: s => s.path,
        view: s => s.view,
        loading: s => s.loading,
        rootNavigationNode: s => s.rootNavigationNode,
        breadcrumbs: s => s.breadcrumbs,

        error(state, getters, rootState, rootGetters) {
            return rootGetters.apiError || rootGetters.loginError || state.error
        },

        resourceApi(state, getters, rootState, rootGetters) {
            const options = {...rootGetters.apiAxiosOptions}
            options.baseURL = options.baseURL + getters.resourceURL
            return axios.create(options)
        },

        resourceURL(state) {
            if (state.path !== null) {
                const encodedParts = []
                for (let part of state.path) {
                    part = encodeURIComponent(part)
                    encodedParts.push(part)
                }
                return encodedParts.join('/')
            }
            return null
        },

    },

}
