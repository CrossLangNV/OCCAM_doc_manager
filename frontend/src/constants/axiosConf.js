let baseUrl = "http://localhost:8000"

if (process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    const baseUrl = process.env.REACT_BASE_URL
}

export {
    baseUrl
};
