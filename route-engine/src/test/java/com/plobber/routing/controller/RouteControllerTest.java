package com.plobber.routing.controller;

import com.plobber.routing.service.RouteResult;
import com.plobber.routing.service.RouteService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(RouteController.class)
class RouteControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private RouteService routeService;

    @Test
    @DisplayName("GET /api/v1/route 호출 시 정상적으로 왕복 경로(Round Trip) 계산 결과를 반환해야 한다.")
    void getRouteTest() throws Exception {
        // given
        RouteRequest request = new RouteRequest();
        request.setLat(35.1769);
        request.setLon(126.9058);
        request.setDistance(5000);
        request.setMode("PLOGGING");

        String mockEncodedPath = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
        RouteResult mockResult = new RouteResult(1500.0, 600000L, mockEncodedPath);
        given(routeService.calculateRoute(request)).willReturn(mockResult);

        // when & then
        mockMvc.perform(get("/api/v1/route")
                .param("lat", String.valueOf(request.getLat()))
                .param("lon", String.valueOf(request.getLon()))
                .param("distance", String.valueOf(request.getDistance()))
                .param("mode", request.getMode()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.distanceMeter").value(1500.0))
                .andExpect(jsonPath("$.timeMillis").value(600000L))
                .andExpect(jsonPath("$.encodedPath").value("_p~iF~ps|U_ulLnnqC_mqNvxq`@"));
    }
}
