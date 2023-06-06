//전역변수 : 현재 폴더 위치
//처음 path="/"
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return ((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

fetch("/api/files/list/")
    .then((response)=>response.json())
    .then((data)=>{
        data.forEach((element)=>{
            resource_id=element.resource_id;
            resource_name=element.resource_name;
            resource_type=element.resource_type;
            sufix_name=element.suffix_name;
            path=element.path;
            is_bookmark=element.is_bookmark;
            is_valid=element.is_valid;
            created_at=element.created_at;
            modified_at=element.modified_at;
            size=formatBytes(element.size,decimals=2);
            parent_resource_id=element.parent_resource_id;
            user_account_id=element.user_account_id;
        })

    })
/*
[
    {
        "resource_id": 1,
        "resource_name": "test",
        "resource_type": "D",
        "suffix_name": "",
        "path": "",
        "is_bookmark": 0,
        "is_valid": 1,
        "created_at": "2023-06-01T21:16:02.606362+09:00",
        "modified_at": "2023-06-01T21:18:01.062931+09:00",
        "size": 2930921,
        "parent_resource_id": null,
        "user_account_id": "abc123"
    }
]
*/

/*

    "resource_id": 8,
    "resource_name": "Update",
    "resource_type": "F",
    "suffix_name": ".exe",
    "path": "test/",
    "is_bookmark": 0,
    "is_valid": 1,
    "created_at": "2023-06-01T21:18:01.057729+09:00",
    "modified_at": "2023-06-01T21:18:01.057764+09:00",
    "size": 1522176,
    "parent_resource_id": 1,
    "user_account_id": "abc123"

*/