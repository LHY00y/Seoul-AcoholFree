var mapOptions = {
    center: new naver.maps.LatLng(map_longitude, map_latitude),
    zoom: 12,
    mapTypeId: 'normal',
    scaleControl: true,
    logoControl: false,
    mapDataControl: true,
    minZoom: 6, // 최소 줌
    zoomControl: true, // 줌 컨트롤 패널 보이기
    zoomControlOptions: {
        style: naver.maps.ZoomControlStyle.LARGE, // 줌 컨트롤 패널 크기
        position: naver.maps.Position.TOP_RIGHT // 줌 컨트롤 패널 위치
    }
};
map = new naver.maps.Map('map', mapOptions);
