# thrift-json

> parse thift idl info to json based on thriftpy

## Installation

```bash
npm i thrift-json
```

## Usage

```javascript
var thriftToJSON = require('thrift-json');
thriftToJSON('/foo/bar.thrift').then(results => console.log(results));
// 或
thriftToJSON(['/foo/bar1.thrift', '/foo/bar2.thrift']).then(results => console.log(results));
```

## Output

Example:

```json
[
    {
        "source": "/foo/bar.thrift",
        "value": {
            "structs": {
                "CityInfo": "{id?:number,name?:string,pinyin?:string,acronym?:string,rank?:string,firstChar?:string}",
                "RecommendRequest": "{userId:number,cityId:number,lat:number,lng:number,uuid:string,poiId?:number}",
                "RecommendInfo": "{itemId?:number,title?:string,imgUrl?:string,score?:string,consumeNum?:number,areaName?:string,lowPrice?:string,saleNum?:number,commentNum?:number,detailUrl?:string,firstCate:Array<number>,avgPrice?:number}",
                "PcHomeCategory": "{id?:number,name?:string,url?:string,pinyin?:string}",
                "HomeCategoryResponse": "{leftPcHomeCategoryList:Array<PcHomeCategory>,rightPcHomeCategoryList:Array<Array<PcHomeCategory>>}",
                "GeneralCategory": "{pcHomeCategory:PcHomeCategory,subPcHomeCategory:Array<PcHomeCategory>}",
                "PoiListCategory": "{pcHomeCategory:PcHomeCategory,generalCategoryList:Array<GeneralCategory>}"
            },
            "services": {
                "WebApiService": {
                    "getNearCity": {
                        "args": "cityId:number",
                        "result": "Array<CityInfo>",
                        "empty": []
                    },
                    "getRecommendInfo": {
                        "args": "req:RecommendRequest",
                        "result": "Array<RecommendInfo>",
                        "empty": []
                    },
                    "getCategory": {
                        "args": "cityId:number",
                        "result": "Array<HomeCategoryResponse>",
                        "empty": []
                    }
                }
            },
            "includes": [
                "common"
            ]
        }
    }
]

the results include:

1. Typescript definition for structs and methods.
1. Empty output for methods.
1. Name of thrift files included.

```