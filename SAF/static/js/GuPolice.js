function fn_searchGu() {
    let poSelect = document.getElementById("poSelect");
    location.href = "/map/" + poSelect.value
}

//구 selector 변경시 지구대/파출소 리스트 selector 변경
function fn_guSelect(gu) {
    let poSelect = document.getElementById("poSelect");
    let poList = gu_json[gu];

    poList = Object.values(poList)
    if (poSelect.options.length > 1) {
        poSelect.options.length = 0;
    }
    for (po in poList) {
        poSelect.options[poSelect.options.length] = new Option(poList[po], poList[po])
    }
}

function findGuArea() {

    var searchGu = "https://api.vworld.kr/req/data?service=data&request=GetFeature&data=LT_C_ADSIGG_INFO&key=D60D697E-DA1B-3C03-B045-CC469028D5FB&domain=127.0.0.1:8000/&attrFilter=sig_kor_nm:like:" + cur_gu;
    if (polyline) {
        polyline.setMap(null);
    }

    fetchJsonp(searchGu)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // 응답 데이터를 처리하고 지도에 경계선을 그리는 작업 수행
            //console.log(data); // 응답 데이터 콘솔에 출력

            // 경계선을 그리기 위한 좌표 데이터 추출
            var coordinates = [];
            //console.log(coordinates)
            var features = data.response.result.featureCollection.features;
            for (var i = 0; i < features[0].geometry.coordinates[0][0].length; i++) {
                var feature = features[0].geometry.coordinates[0][0][i];
                var x = feature[0];
                var y = feature[1];
                coordinates.push(new naver.maps.LatLng(y, x));
                var location = new naver.maps.LatLng(features[0].geometry.coordinates[0][0][200])
            }
            // 경계선 생성
            polyline = new naver.maps.Polyline({
                path: coordinates,
                strokeColor: '#0000FF', // 선 색
                strokeOpacity: 0.8, // 투명도
                strokeWeight: 6,
                zIndex: 2,
                clickable: true,
                map: map // 위에서 생성한 지도에 추가
            });
            map.setCenter(location);
        })
        .catch(function (error) {
            console.log('API 요청 중 오류 발생:', error);
        });
}

