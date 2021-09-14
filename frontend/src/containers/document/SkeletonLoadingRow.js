import React from 'react';
import {Skeleton} from "primereact/skeleton";

const SkeletonLoadingRow = () => {
    return (
        <tr>
            <td className='w-10 occ-doc-list-td'>
                <Skeleton className={"page-list-loading"} width={"100px"} height={"160px"}/>
            </td>
            <td className='w-50 occ-doc-list-td'>
                <Skeleton className={"page-list-loading"} width={"90%"}/>
            </td>
            <td className="occ-doc-list-td">
                <Skeleton className={"page-list-loading"} width={"128px"}/>
            </td>
            <td className='w-10 occ-doc-list-td'>
                <Skeleton className={"page-list-loading"} width={"128px"}/>
            </td>
            <td className='w-10 occ-doc-list-td'>
                <Skeleton className={"page-list-loading"} width={"37.7px"} height={"42px"}/>
            </td>
        </tr>
    );
};

export default SkeletonLoadingRow;
