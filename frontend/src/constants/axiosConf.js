import axios from "axios";

const token = localStorage.getItem("access");
let axiosConfig = {baseURL: 'http://localhost:8000',
    timeout: 1000,
    headers: {
        'Authorization' : token ? `Bearer ${token}` : ''
    }
};

let axiosApi = axios.create(axiosConfig);

export {
    axiosConfig,
    axiosApi
};
