package com.plobber.routing.controller;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
public record RouteRequest(
    @NotNull(message = "위도(lat)는 필수입니다.")
    @Min(value = -90, message = "위도는 -90 이상이어야 합니다.")
    @Max(value = 90, message = "위도는 90 이하이어야 합니다.")
    Double lat,

    @NotNull(message = "경도(lon)는 필수입니다.")
    @Min(value = -180, message = "경도는 -180 이상이어야 합니다.")
    @Max(value = 180, message = "경도는 180 이하이어야 합니다.")
    Double lon,

    @Min(value = 500, message = "왕복 거리는 최소 500m 이상이어야 합니다.")
    @Max(value = 30000, message = "왕복 거리는 최대 30km(30000m)를 넘을 수 없습니다.")
    Integer distance,

    String mode
) {
    public RouteRequest {
        if (distance == null) distance = 5000;
        if (mode == null) mode = "PLOGGING";
    }
}
