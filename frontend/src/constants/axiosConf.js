let baseUrl
let clientId
let clientSecret
let googleOauthKey

console.log(process.env.NODE_ENV)

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

console.log(baseUrl)
console.log(clientId)
console.log(clientSecret)
console.log(googleOauthKey)



export {
    baseUrl,
    clientId,
    clientSecret,
    googleOauthKey
};
