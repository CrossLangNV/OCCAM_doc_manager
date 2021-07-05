let baseUrl
let clientId
let clientSecret
let googleOauthKey

const logging = false;

if (process.env.NODE_ENV === 'production') {
    baseUrl = window._env_.REACT_APP_API_URL
    clientId = window._env_.REACT_DJANGO_CLIENT_ID
    clientSecret = window._env_.REACT_DJANGO_CLIENT_SECRET
    googleOauthKey = window._env_.REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY

    if (logging) {
        console.log("Production build")
    }
} else {
    baseUrl = process.env.REACT_APP_API_URL
    clientId = process.env.REACT_APP_DJANGO_CLIENT_ID
    clientSecret = process.env.REACT_APP_DJANGO_CLIENT_SECRET
    googleOauthKey = process.env.REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY

    if (logging) {
        console.log("Development build")
    }
}

if (logging) {
    console.log("Build: ", process.env.NODE_ENV)
    console.log("baseUrl: ", baseUrl)
    console.log("clientId: ", clientId)
    console.log("clientSecret: ", clientSecret)
    console.log("googleOauthKey: ", googleOauthKey)
}

export {
    baseUrl,
    clientId,
    clientSecret,
    googleOauthKey
};
