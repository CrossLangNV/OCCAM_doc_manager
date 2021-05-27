let baseUrl = "http://localhost:8000"

if (process.env.NODE_ENV === 'production') {
    baseUrl = process.env.REACT_APP_API_URL
}

console.log(process.env.NODE_ENV)
console.log(baseUrl)

console.log(process.env.REACT_APP_API_URL)
console.log(process.env.REACT_APP_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)


export {
    baseUrl
};
