package com.plobber.routing.graphhopper;

import com.graphhopper.reader.ReaderWay;
import com.graphhopper.routing.ev.DecimalEncodedValue;
import com.graphhopper.routing.ev.DecimalEncodedValueImpl;
import com.graphhopper.routing.ev.EdgeIntAccess;
import com.graphhopper.routing.util.parsers.TagParser;
import com.graphhopper.storage.IntsRef;
import com.plobber.routing.repository.HotspotRepository;

public class PloggingTagParser implements TagParser {

    private final HotspotRepository hotspotRepository;
    private final DecimalEncodedValue trashProbEnc;

    public PloggingTagParser(HotspotRepository hotspotRepository) {
        this.hotspotRepository = hotspotRepository;
        this.trashProbEnc = new DecimalEncodedValueImpl("trash_prob", 5, 0.032258, 0, false, false, false);
    }

    @Override
    public void handleWayTags(int edgeId, EdgeIntAccess edgeIntAccess, ReaderWay way, IntsRef relationFlags) {
    }
}
