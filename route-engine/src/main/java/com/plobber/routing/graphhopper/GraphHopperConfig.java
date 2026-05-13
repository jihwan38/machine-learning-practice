package com.plobber.routing.graphhopper;

import com.graphhopper.GraphHopper;
import com.graphhopper.config.Profile;
import com.graphhopper.routing.ev.DefaultImportRegistry;
import com.graphhopper.routing.ev.ImportUnit;
import com.graphhopper.util.CustomModel;
import com.plobber.routing.repository.HotspotRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GraphHopperConfig {

    @Bean
    public GraphHopper graphHopper(
            HotspotRepository hotspotRepository,
            @Value("${graphhopper.datareader.file:data/seoul.osm.pbf}") String osmFilePath,
            @Value("${graphhopper.graph.location:target/routing-graph-cache}") String graphCacheLocation
    ) {
        GraphHopper hopper = new GraphHopper();
        hopper.setOSMFile(osmFilePath);
        hopper.setGraphHopperLocation(graphCacheLocation);

        CustomModel footBaseModel = new CustomModel();
        footBaseModel.addToSpeed(com.graphhopper.json.Statement.If("true", com.graphhopper.json.Statement.Op.LIMIT, "5"));
        footBaseModel.addToPriority(com.graphhopper.json.Statement.If("road_class == MOTORWAY || road_class == TRUNK", com.graphhopper.json.Statement.Op.MULTIPLY, "0"));
        
        hopper.setProfiles(new Profile("plogging_foot").setCustomModel(footBaseModel));

        PloggingTagParser parser = new PloggingTagParser(hotspotRepository);
        
        hopper.setEncodedValuesString("trash_prob");
        hopper.setImportRegistry(new DefaultImportRegistry() {
            @Override
            public ImportUnit createImportUnit(String name) {
                if ("trash_prob".equals(name)) {
                    return ImportUnit.create("trash_prob", 
                            map -> parser.getTrashProbEnc(), 
                            (lookup, map) -> parser
                    );
                }
                return super.createImportUnit(name);
            }
        });
        
        return hopper;
    }
}
