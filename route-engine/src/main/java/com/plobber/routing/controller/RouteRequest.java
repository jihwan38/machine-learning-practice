package com.plobber.routing.controller;

import lombok.Data;

@Data
public class RouteRequest {
    private Double lat;
    private Double lon;
    private Integer distance = 5000;
    private String mode = "PLOGGING";
}
