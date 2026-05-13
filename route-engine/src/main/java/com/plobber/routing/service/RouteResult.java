package com.plobber.routing.service;

public class RouteResult {
    private final double distanceMeter;
    private final long timeMillis;
    private final String encodedPath;

    public RouteResult(double distanceMeter, long timeMillis, String encodedPath) {
        this.distanceMeter = distanceMeter;
        this.timeMillis = timeMillis;
        this.encodedPath = encodedPath;
    }

    public double getDistanceMeter() {
        return distanceMeter;
    }

    public long getTimeMillis() {
        return timeMillis;
    }
    
    public String getEncodedPath() {
        return encodedPath;
    }
}
