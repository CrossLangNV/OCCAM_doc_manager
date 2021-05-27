let baseUrl = "http://localhost:8000"

if (process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    baseUrl = process.env.DJANGO_BASE_URL
}

export {
    baseUrl
};
