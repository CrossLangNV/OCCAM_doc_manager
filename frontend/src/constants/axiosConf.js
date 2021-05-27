let baseUrl = "http://localhost:8000"

if (process.env.NODE_ENV === 'production') {
    baseUrl = process.env.REACT_APP_API_URL
}

console.log(baseUrl)
console.log(process.env.NODE_ENV)

export {
    baseUrl
};
