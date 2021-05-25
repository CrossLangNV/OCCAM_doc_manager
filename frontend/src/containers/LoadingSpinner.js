import React from 'react';

const LoadingSpinner = () => {
    return (
        <span className='margin-left'>
            <i className="pi pi-spin pi-spinner"
               style={{'fontSize': '2em'}}/>
        </span>
    );
};

export default LoadingSpinner;
