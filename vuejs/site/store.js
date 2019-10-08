
import { mapGetters } from 'vuex'
import axios from 'axios'

export default {

    state: {
        user_email: null,
        user_uuid: null,
        loginError: null,
    },

    mutations: {

        siteSetSessionInfo(state, sessionInfo) {
            if (sessionInfo.user) {
                state.user_email = sessionInfo.user.user_email
                state.user_uuid = sessionInfo.user.user_uuid
            } else {
                state.user_email = null
                state.user_uuid = null
            }
        },

        siteSetLoginError(state, error) {
            state.loginError = error
        },

    },

    actions: {

        setSessionInfo(context, options) {
            context.commit('siteSetSessionInfo', options.sessionInfo)
        },

        passwordLogin(context, options) {
            context.getters.api({
                method: 'post',
                url: '@@login',
                auth: {
                    username: options.username,
                    password: options.password,
                }
            }).then(response => {
                context.dispatch('refreshSessionInfo')
            }).catch(error => {
                context.commit('siteSetLoginError', error)
            })
        },

    },

    getters: {
        loginError: s => s.loginError,
        user_email: s => s.user_email,
    },

}
