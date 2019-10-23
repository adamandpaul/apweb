
import axios from 'axios'

const DEFAULT_ROOT_NAVIGATION_NODE = {
    "title": "App",
    "path": [""],
    "named_resources": [],
}

export default {

    state: {
        path: null,
        views: [],
        loading: true,
        error: null,
        description: null,
        breadcrumbs: [DEFAULT_ROOT_NAVIGATION_NODE],
        rootNavigationNode: DEFAULT_ROOT_NAVIGATION_NODE,
    },

    mutations: {
        loadingStart(state, path) {
            state.path = path
            state.loading = true
            state.error = null

            // reset current workspace state
            state.description = null
            state.breadcrumbs = [state.rootNavigationNode]
            state.views = []
        },
        loadingComplete(state, data) {
            state.loading = false
            state.error = null

            // set workspace state
            state.description = data.description
            state.breadcrumbs = data.breadcrumbs
            const views = []
            for (let v in data.views) {
                views.push({
                    "name": v,
                    ...data.views[v],
                })
            }
            views.sort((a, b) => (a.sort_key - b.sort_key))
            state.views = views

            // Save root navigation node
            state.rootNavigationNode = state.breadcrumbs[0]
        },
        loadingError(state, error) {
            state.loading = false
            state.error = error
        },
    },

    actions: {
        loadResource(context, opts) {
            context.commit('loadingStart', opts.path)
            context.getters.resourceApi.get("@@admin")
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
    },

    getters: {
        path: s => s.path,
        loading: s => s.loading,
        rootNavigationNode: s => s.rootNavigationNode,
        description: s => s.description,
        breadcrumbs: s => s.breadcrumbs,
        namedResources: s => s.breadcrumbs[s.breadcrumbs.length - 1].named_resources,
        viewsList: s => s.views,
        viewsByName(state, getters) {
            const views = {}
            for (let v of getters.viewsList) {
                views[v.name] = v
            }
            return views
        },
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
                return encodedParts.join('/') || "/"
            }
            return null
        },

    },

}
