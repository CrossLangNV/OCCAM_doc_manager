let baseUrl
let clientId
let clientSecret
let googleOauthKey

if (process.env.NODE_ENV === 'production') {
    baseUrl = window._env_.REACT_APP_API_URL
    clientId = window._env_.REACT_DJANGO_CLIENT_ID
    clientSecret = window._env_.REACT_DJANGO_CLIENT_SECRET
    googleOauthKey = window._env_.REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
} else {
    baseUrl = process.env.REACT_APP_API_URL
    clientId = process.env.REACT_APP_DJANGO_CLIENT_ID
    clientSecret = process.env.REACT_APP_DJANGO_CLIENT_SECRET
    googleOauthKey = process.env.REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
}

export {
    baseUrl,
    clientId,
    clientSecret,
    googleOauthKey
};
