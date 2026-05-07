package com.plobber.routing.repository;

public interface HotspotRepository {
    double findProbabilityByPoint(double lat, double lon);
}
