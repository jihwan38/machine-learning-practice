package com.plobber.routing.repository;

import org.springframework.stereotype.Repository;

public interface HotspotRepository {
    double findProbabilityByPoint(double lat, double lon);
}
