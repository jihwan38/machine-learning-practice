package com.plobber.routing.graphhopper;

import com.graphhopper.GraphHopper;
import com.plobber.routing.repository.HotspotRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import com.graphhopper.routing.ev.ImportRegistry;
import com.graphhopper.routing.ev.ImportUnit;

import static org.assertj.core.api.Assertions.assertThat;

@ExtendWith(MockitoExtension.class)
class GraphHopperConfigTest {

    @Mock
    private HotspotRepository hotspotRepository;

    @Test
    @DisplayName("GraphHopper 객체 생성 시 PloggingTagParser가 정상 등록되어야 한다.")
    void graphHopperBeanCreationTest() {
        //given
        GraphHopperConfig config = new GraphHopperConfig();
        
        // when & then
        GraphHopper hopper = config.graphHopper(hotspotRepository, "dummy.osm.pbf", "target/dummy-cache");
        
        assertThat(hopper).isNotNull();
        assertThat(hopper.getGraphHopperLocation()).isEqualTo("target/dummy-cache");
        assertThat(hopper.getProfiles()).hasSize(1);
        assertThat(hopper.getProfiles().get(0).getName()).isEqualTo("plogging_foot");
        

        ImportRegistry registry = hopper.getImportRegistry();
        assertThat(registry).isNotNull();
        
        ImportUnit unit = registry.createImportUnit("trash_prob");
        assertThat(unit).isNotNull();
        assertThat(unit.getCreateEncodedValue()).isNotNull();
        assertThat(unit.getCreateTagParser()).isNotNull();
    }
}
