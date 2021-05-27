let baseUrl = "http://localhost:8000"

if (process.env.NODE_ENV === 'production') {
    baseUrl = process.env.DJANGO_BASE_URL
}

export {
    baseUrl
};
