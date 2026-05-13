package com.plobber.routing.repository;

import org.springframework.stereotype.Repository;

@Repository
public interface HotspotRepository {
    double findProbabilityByPoint(double lat, double lon);
}
